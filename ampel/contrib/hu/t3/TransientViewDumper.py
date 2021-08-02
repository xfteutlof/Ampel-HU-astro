#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/contrib/hu/t3/TransientInfoDumper.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 15.08.2018
# Last Modified Date: 15.08.2018
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

import json, uuid, requests
from gzip import GzipFile
from io import BytesIO
from typing import Optional, Tuple
from urllib.parse import ParseResult, urlencode, urlparse, urlunparse
from xml.etree import ElementTree
from ampel.abstract.AbsT3Unit import AbsT3Unit
from ampel.abstract.Secret import Secret
from ampel.util.json import AmpelEncoder
from ampel.view.SnapView import SnapView
from ampel.view.TransientView import TransientView


def strip_auth_from_url(url):
    try:
        auth = requests.utils.get_auth_from_url(url)
        scheme, netloc, path, params, query, fragment = urlparse(url)
        netloc = netloc[netloc.index("@") + 1 :]
        url = urlunparse(ParseResult(scheme, netloc, path, params, query, fragment))
        return url, auth
    except KeyError:
        return url, None


def strip_path_from_url(url):
    scheme, netloc, path, params, query, fragment = urlparse(url)
    return urlunparse(ParseResult(scheme, netloc, "/", None, None, None))


class TransientViewDumper(AbsT3Unit):
    """"""

    version = 0.1
    resources = ("desycloud",)

    outputfile: Optional[str] = None
    desycloud_auth: Secret[dict] = {"key": "desycloud"}  # type: ignore[assignment]

    def post_init(self) -> None:
        self.count = 0
        if not self.outputfile:
            self.outfile = GzipFile(fileobj=BytesIO(), mode="w")
            self.path = "/AMPEL/dumps/" + str(uuid.uuid1()) + ".json.gz"
            self.session = requests.Session()
            assert self.resource
            self.webdav_base = self.resource["desycloud"]
            self.ocs_base = (
                strip_path_from_url(self.resource["desycloud"])
                + "/ocs/v1.php/apps/files_sharing/api/v1"
            )
        else:
            self.outfile = GzipFile(self.outputfile + ".json.gz", mode="w")
        # don't bother preserving immutable types
        self.encoder = AmpelEncoder(lossy=True)


    def process(self, transients: Tuple[SnapView, ...]) -> None:

        if transients is not None:

            batch_count = len(transients)
            self.count += batch_count

            for tran_view in transients:
                self.outfile.write(self.encoder.encode(tran_view).encode("utf-8"))
                self.outfile.write(b"\n")

        self.outfile.flush()
        self.logger.info("Total number of transient printed: %i" % self.count)
        if self.outputfile:
            self.outfile.close()
            self.logger.info(self.outputfile + ".json.gz")
        else:
            assert isinstance(self.outfile.fileobj, BytesIO)
            mb = len(self.outfile.fileobj.getvalue()) / 2.0 ** 20
            self.logger.info("{:.1f} MB of gzipped JSONy goodness".format(mb))
            self.session.put(
                self.webdav_base + self.path,
                data=self.outfile.fileobj.getvalue(),
                auth=self.desycloud_auth.get(),
            ).raise_for_status()
            response = self.session.post(
                self.ocs_base + "/shares",
                data=dict(path=self.path, shareType=3),
                auth=self.desycloud_auth.get(),
                headers={"OCS-APIRequest": "true"},  # i'm not a CSRF attack, i swear
            )
            self.outfile.close()
            if response.ok and (
                element := ElementTree.fromstring(response.text).find("data/url")
            ):
                if element.text:
                    self.logger.info(element.text)
            else:
                response.raise_for_status()
