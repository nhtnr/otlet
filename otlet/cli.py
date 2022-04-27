"""
otlet.cli - otlet command line tool
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

import os
import signal
import textwrap
from argparse import ArgumentParser
from . import __version__, api, exceptions


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
        "--releases", help="print list of releases for package", action="store_true"
    )
    parser.add_argument(
        "--vulnerabilities",
        help="print information about known vulnerabilities for package release version",
        action="store_true",
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


def print_releases(package: str):
    pkg = api.get_full(package)
    for rel in pkg.releases:
        print(rel)

    raise SystemExit(0)


def print_vulns(package: str, version: str):
    pkg = api.get_release_full(package, version)

    if pkg.vulnerabilities is None:
        print("No vulnerabilities found for this release! :)")
        raise SystemExit(0)

    os.system("clear" if os.name != "nt" else "cls")
    print(
        "==",
        len(pkg.vulnerabilities),
        "security vulnerabilities found for",
        pkg.release_name,
        "==\n",
    )

    for vuln in pkg.vulnerabilities:
        print(
            pkg.vulnerabilities.index(vuln) + 1, "/", len(pkg.vulnerabilities), sep=""
        )
        msg = ""
        msg += f"\u001b[1m{vuln.id} ({', '.join(vuln.aliases).strip(', ')})\u001b[0m\n"
        msg += textwrap.TextWrapper(initial_indent="\t", subsequent_indent="\t").fill(
            vuln.details
        )
        msg += f"\n\u001b[1mFixed in version(s):\u001b[0m '{', '.join(vuln.fixed_in).strip(', ')}'\n"
        msg += f"(See more: '{vuln.link}')\n"
        print(msg)
        input("== Press ENTER for next page ==")
        os.system("clear" if os.name != "nt" else "cls")

    raise SystemExit(0)


def main():
    signal.signal(
        signal.SIGINT, lambda *_: (_ for _ in ()).throw(SystemExit(0))
    )  # no yucky exception on KeyboardInterrupt (^C)
    args = init_args()

    if args.releases:
        print_releases(args.package[0])

    if args.vulnerabilities and len(args.package) > 1:
        print_vulns(args.package[0], args.package[1])
    elif args.vulnerabilities and not len(args.package) > 1:
        raise SystemExit(
            "Please supply both a package AND a package version, i.e. 'otlet django 3.1.0 --vulnerabilities'"
        )

    try:
        if len(args.package) > 1:
            pkg = api.get_release_full(args.package[0], args.package[1])
        else:
            pkg = api.get_full(args.package[0])
    except exceptions.PyPIAPIError as err:
        raise SystemExit(f"{args.package[0]}: " + err.__str__())

    indent_chars = "\n\t\t"
    msg = textwrap.dedent(
        f"""Info for package {pkg.name} v{pkg.version}

    Summary: {pkg.info.summary}
    Release date: {f"{pkg.upload_time.date()} at {pkg.upload_time.astimezone().timetz()}" if pkg.upload_time else "N/A"}
    URL: {pkg.info.package_url}
    Author: {pkg.info.author} <{pkg.info.author_email}>
    License: {pkg.info.license}
    Python Version(s): {pkg.info.requires_python if pkg.info.requires_python else "Not Defined"}
    Dependencies: ({len(pkg.info.requires_dist) if pkg.info.requires_dist else 0}) \n\t\t{indent_chars.join(pkg.info.requires_dist) if pkg.info.requires_dist else ""}
    """
    )
    if pkg.vulnerabilities:
        msg += "\n==WARNING==\nThis version has known security vulnerabilities, use the '--vulnerabilities' flag to view them\n"
    if pkg.info.yanked:
        msg += f"\n==NOTE==\nThis version has been yanked from PyPI.\n\t Reason: '{pkg.info.yanked_reason}'\n"
    print(msg)
    raise SystemExit(0)
