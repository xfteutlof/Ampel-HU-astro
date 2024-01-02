#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-contrib-HU/ampel/contrib/hu/t3/TigreTablePublisher.py
# License:             BSD-3-Clause
# Author:              felix.arnon.teutloff@studium.uni-hamburg.de
# Date:                15.12.2023

from functools import reduce
from typing import Any, Optional, Union
from collections.abc import Generator
import re, os, requests, io, backoff
import pandas as pd

from ampel.types import UBson, T3Send
from ampel.secret.NamedSecret import NamedSecret
from ampel.abstract.AbsT3ReviewUnit import AbsT3ReviewUnit
from ampel.abstract.AbsPhotoT3Unit import AbsPhotoT3Unit
from ampel.view.TransientView import TransientView
from ampel.struct.UnitResult import UnitResult
from ampel.struct.T3Store import T3Store
from ampel.view.SnapView import SnapView
from ampel.util.mappings import get_by_path
from paramiko import SSHClient, AutoAddPolicy, RSAKey

class TigreTablePublisher(AbsPhotoT3Unit):
    """

    Construct a table based on selected T2 output values.
    Current output format can be csv or latex.
    Table can optionally saved to a local file or sent to remote directory via sftp.

    Config parameters:
    include_stock (bool)
    include_channels (bool)

    How to deal with names. Will search each transients names for entries containing "value",
    and return any output under "key"
    name_filter = { 'ZTF name' : 'ZTF', 'TNS ID' : 'TNS' }

    Selection of fields to save. Matches structure of t2document result dict, e.g.:
    table_schema = { { 't2_unit'  : {
                'table_label_1' : ['path','to','val'],
            'table_label_2' : ['other','path']
            },
        } }
    transient_table_schema = { { 'point_t2_unit'  : {
                'table_label_1' : ['path','to','val'],
            'table_label_2' : ['other','path']
            },
        } }

    Output format (converted through pandas)
    fmt = 'csv'     # Current options 'csv', 'latex'.

    Destination attempted if the appropriate  parameters are set for
    file_name
    local save:
      local_path
    host_server
    host_user
    priv_key_path

    """

    # Two tables describing what information to save into the table.
    # Schema for state dependent T2s (one row for each)
    table_schema: dict[str, Any]
    # Schema for transient dependent T2s (added to each row together with base info)
    transient_table_schema: dict[str, Any]

    name_filter: dict[str, str] = {'ZTF name': 'ZTF', 'TNS ID': 'TNS'}
    include_stock: bool = False
    include_channels: bool = True
    # Add also transients lacking any T2 info
    save_base_info: bool = False

    fmt: str = 'csv'

    file_name: str = 'TransientTable.csv'
    local_path: None | str = None

    remote_path: NamedSecret[str] = None
    sftp_send_info: NamedSecret[dict] = None

    def process(self, gen: Generator[TransientView, T3Send, None],
                t3s: Optional[T3Store] = None) -> Union[UBson, UnitResult]:
#    def process(self, gen: Generator[SnapView, T3Send, None], t3s: T3Store) -> None:
        """
        Loop through provided TransientViews and extract data according to the
        configured schema.
        """


        table_rows: list[dict[str, Any]] = []
        for k, tran_view in enumerate(gen, 1):


            basetdict: dict[str, Any] = {}
            # Assemble t2 information bound to the transient (e.g. Point T2s)
            for t2unit, table_entries in self.transient_table_schema.items():
                # New SnapView has method for directly retrieve result.
                # Possibly use this.
                if isinstance(t2res := tran_view.get_latest_t2_body(unit=t2unit), dict):
                    for label, path in table_entries.items():
                        basetdict[label] = get_by_path(t2res, path)

            # Assemble info which could vary from state to state
            # Should add config to labels if multiple exports
            # from same unit is requested.
            stateinfo = []
            for t1_document in tran_view.t1 or []:
                t1_link = t1_document['link']
                tdict = {}
                for t2unit, table_entries in self.table_schema.items():
                    if isinstance(t2res := tran_view.get_latest_t2_body(unit=t2unit, link=t1_link), dict):
                        for label, path in table_entries.items():
                            tdict[label] = get_by_path(t2res, path)
                if len(tdict) > 0:
                    stateinfo.append(tdict)

            if len(stateinfo) == 0 and len(basetdict.keys()) == 0 and not self.save_base_info:
                continue

            # Collect base information applying to all states
            # If here, add stock info (name, channel etcs)
            if names := (tran_view.stock or {}).get("name", []):
                for label, name_str in self.name_filter.items():
                    r = re.compile(name_str)
                    # While names will mostly be unique, it might not always be the case.
                    basetdict[label] = list(filter(r.match, names)) # type: ignore[arg-type]
                    # Avoid list when possible
                    if isinstance((item := basetdict[label]), (list, tuple)) and len(item) == 1:
                        basetdict[label] = item[0]

            if self.include_stock:
                basetdict['stock'] = tran_view.id
            if self.include_channels and tran_view.stock:
                channels = tran_view.stock.get("channel")
                # Allow for both single (most common) and duplacte channels.
                basetdict['channels'] = channels[0] if isinstance(channels, (list, tuple)) and len(channels) == 1 else channels

            # Collect and add to table
            if len(stateinfo) > 0:
                for tdict in stateinfo:
                    tdict.update(basetdict)
                    table_rows.append(tdict)
            else:
                # Only transient info
                table_rows.append(basetdict)

        self.logger.info("", extra={'table_count': len(table_rows)})
        if len(table_rows) == 0:
            return None

        # Export assembled information
        # Convert
        df = pd.DataFrame.from_dict(table_rows)

        # Local save
        if self.local_path is not None:
            full_path = os.path.join(self.local_path, self.file_name)
            if self.fmt == 'csv':
                df.to_csv(full_path)
            elif self.fmt == 'latex':
                df.to_latex(full_path)
            self.logger.info('Exported', extra={'path': full_path})

        # Export to slack if requested
        self._sftp_export(df)

        # Could potentially return a document to T3 collection detailing
        # what was done, as well as the table itself.
        return None


    @backoff.on_exception(
        backoff.expo,
        requests.ConnectionError,
        max_tries=5,
        factor=10,
    )
    def _sftp_export(self, df):
        """
        Export content of Pandas dataframe to remote directory.
        """
        sftp_dict = self.sftp_send_info.get()
        if sftp_dict['hostname'] is None or sftp_dict['username'] is None or \
        (sftp_dict['key_filename'] is None and sftp_dict['pkey'] is None and sftp_dict['password'] is None):
            return
        if self.remote_path is None:
            self.remote_path = "./"

        if sftp_dict['pkey'] is not None:
            private_key_file = io.StringIO(sftp_dict['pkey'])
            private_key = RSAKey.from_private_key(private_key_file)
            sftp_dict['pkey'] = private_key
        
        buffer = io.StringIO(self.file_name)
        if self.fmt == 'csv':
            df.to_csv(buffer)
        elif self.fmt == 'latex':
            df.to_latex(buffer)

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(look_for_keys = False, **sftp_dict)
        sftp = ssh.open_sftp()
        
        with sftp.open(self.remote_path.get()+self.file_name, "w") as f:
            f.write(buffer.getvalue())

        sftp.close()
        ssh.close()

        self.logger.info("sftp sent")

        return
