#!/usr/bin/env python3

"""
Generate a Markdown-formatted list of Ampel units provided by this package
"""

import inspect
import re
import sys
from argparse import ArgumentParser
from contextlib import contextmanager
from pathlib import Path

from ampel.config.AmpelConfig import AmpelConfig
from ampel.config.builder.DisplayOptions import DisplayOptions
from ampel.config.builder.DistConfigBuilder import DistConfigBuilder
from ampel.core.UnitLoader import UnitLoader

parser = ArgumentParser()
parser.add_argument(
    "--target-file", help="append list to a file. if omitted, print to stdout"
)
parser.add_argument("-d", "--distribution", nargs="+", help="distributions to include")
args = parser.parse_args()


def is_abstract(klass: type) -> bool:
    from ampel.base.AmpelABC import _raise_error

    return klass.__new__ is _raise_error


def relative_path_in_repo(path: Path) -> Path | None:
    """Get path relative to the nearest git repo"""
    for parent in path.parents:
        if (parent / ".git").exists():
            return path.relative_to(parent)
    return None


@contextmanager
def open_target_file():
    if args.target_file:
        with open(args.target_file, "r+") as fileobj:
            content: str = fileobj.read()
            fileobj.seek(content.index(TAG))
            fileobj.truncate(fileobj.tell())
            fileobj.write(TAG)
            yield fileobj
    else:
        yield sys.stdout


cb = DistConfigBuilder(
    options=DisplayOptions(
        verbose=False,
        hide_stderr=True,
        hide_module_not_found_errors=False,
    ),
)

TARGET_DISTS = set(args.distribution)

cb.load_distributions()
config = AmpelConfig(cb.build_config(get_unit_env=False, config_validator=None))

loader = UnitLoader(config, db=None, provenance=False)

bases = {
    "T0 units (alert filters)": ["AbsAlertFilter"],
    "T2 units (augment)": ["AbsPointT2Unit", "AbsTiedT2Unit", "AbsCustomStateT2Unit"],
    "T3 units (react)": ["AbsT3PlainUnit", "AbsT3ReviewUnit"],
}
categories = {base: category for category, bases in bases.items() for base in bases}
docs = {k: {} for k in bases}

for name, spec in config.get("unit").items():
    if spec["distrib"] not in TARGET_DISTS or not set(spec["base"]).intersection(
        categories
    ):
        continue
    category = next(categories[base] for base in spec["base"] if base in categories)
    unit = loader.get_class_by_name(name)
    if is_abstract(unit):
        continue
    if (
        unit.__doc__
        and unit.__doc__.strip()
        and not any(unit.__doc__ == base.__doc__ for base in unit.__bases__)
    ):
        # extract the first sentence (ends with punctuation followed by something other than a lowercase letter), unwrap, and add a period
        doc = re.split(
            r"([\.!\?:]\s+?([^a-z]|\n)|\n\n)",
            inspect.getdoc(unit).strip(),
            maxsplit=1,
            flags=re.MULTILINE,
        )[0].strip()
        doc = re.sub(r"\s*\n\s*", " ", doc) + "."
    else:
        doc = None
    docs[category][name] = (unit, doc)

TAG = "<!-- AUTOGENERATED CONTENT, do not edit below this line -->\n"

with open_target_file() as fileobj:
    for category in docs:
        print(f"\n### {category}:", file=fileobj)
        for name in sorted(docs[category].keys()):
            unit, doc = docs[category][name]
            print(
                f"- [{name}]({relative_path_in_repo(Path(sys.modules[unit.__module__].__file__))})",
                end="",
                file=fileobj,
            )
            if doc:
                print(f": {doc}", end="", file=fileobj)
            print(file=fileobj)
