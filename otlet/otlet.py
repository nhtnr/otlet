"""
otlet.otlet - otlet cli tool
CLI tool and wrapper for PyPI JSON Web API

Copyright (c) 2022 Noah Tanner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""

import textwrap
import time
from argparse import ArgumentParser
from . import __version__
from . import *
from .exceptions import PyPIAPIError


def init_args():
    parser = ArgumentParser(
        prog="otlet",
        epilog="(c) 2022-present Noah Tanner, released under the terms of the MIT License",
    )
    parser.add_argument(
        "package",
        metavar=("package [VERSION]"),
        default=[],
        nargs="*",
        type=str,
        help="The package to search for. (version is optional)",
    )
    parser.add_argument(
        "--releases",
        help="print list of releases for package",
        action="store_true"
    )
    parser.add_argument(
        "-v",
        "--version",
        help="print version information and exit",
        action="store_true",
    )

    args = parser.parse_args()
    if args.version:
        print(
            textwrap.dedent(
                f"""
                        otlet v{__version__}
                        (c) 2022-present Noah Tanner, released under the terms of the MIT License"""
            )
        )
        raise SystemExit(0)
    if not args.package:
        raise SystemExit(
            "Please supply a package to search for: i.e. 'otlet sampleproject'"
        )

    return args

def fetch_releases(package: str):
    pkg = get_full(package)
    for rel in pkg.releases:
        print(rel)

    raise SystemExit(0)

def main():
    args = init_args()
    if args.releases:
        fetch_releases(args.package[0])

    try:
        if len(args.package) > 1:
            pkg = get_release_full(args.package[0], args.package[1])
        else:
            pkg = get_full(args.package[0])
    except PyPIAPIError as err:
        raise SystemExit(f"{args.package[0]}: " + err.__str__())

    indent_chars = "\n\t\t"
    print(
        textwrap.dedent(
            f"""Info for package {pkg.info.name} v{pkg.info.version}

    Summary: {pkg.info.summary}
    Release date: {f"{pkg.upload_time.date()} at {pkg.upload_time.astimezone().timetz()}" if pkg.upload_time else "N/A"}
    URL: {pkg.info.package_url}
    Author: {pkg.info.author} <{pkg.info.author_email}>
    License: {pkg.info.license}
    Python Version(s): {pkg.info.requires_python if pkg.info.requires_python else "Not Defined"}
    Dependencies: ({len(pkg.info.requires_dist) if pkg.info.requires_dist else 0}) \n\t\t{indent_chars.join(pkg.info.requires_dist) if pkg.info.requires_dist else ""}
    {f"==NOTE== This version has been yanked from PyPI. (Reason: {pkg.info.yanked_reason})" if pkg.info.yanked else ""}"""
        )
    )

    raise SystemExit(0)
