"""
otlet.cli
======================
CLI tool for returning PyPI package information, using the otlet wrapper
"""
#
# Copyright (c) 2022 Noah Tanner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import os
import signal
import textwrap
from . import util
from .options import OtletArgumentParser
from .. import __version__, api, exceptions



def init_args():
    parser = OtletArgumentParser()

    args = parser.parse_args()
    if args.version:
        WHITE = "\u001b[38;5;255m" if os.environ.get("TERM") == "xterm-256color" else "\u001b[37m"
        CYAN = "\u001b[38;5;153m" if os.environ.get("TERM") == "xterm-256color" else "\u001b[36m"
        print(
            textwrap.dedent(
                f"""
                        {CYAN}°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸

                        {WHITE}otlet v{__version__}
                        {WHITE}(c) 2022-present Noah Tanner, released under the terms of the MIT License

                        {CYAN}°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸ \u001b[0m
                """ # ascii art sourced from http://1lineart.kulaone.com
            )
        )
        raise SystemExit(0)
    if not args.package:
        raise SystemExit(
            "Please supply a package to search for: i.e. 'otlet sampleproject'"
        )
    if parser.__dict__.get("subparsers"):
        args.__dict__["subparsers"] = []
        for s in parser.__dict__.get("subparsers").choices:
            args.__dict__["subparsers"].append(s)

    else:
        args.__dict__["subparsers"] = None

    return args


def main():

    signal.signal(
        signal.SIGINT, lambda *_: (_ for _ in ()).throw(SystemExit(0))
    )  # no yucky exception on KeyboardInterrupt (^C)
    args = init_args()

    if args.subparsers:
        util.print_releases(args)
    if args.urls:
        util.print_urls(args.package[0])

    if args.vulnerabilities and len(args.package) > 1:
        util.print_vulns(args.package[0], args.package[1])
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
        f"""Info for package {pkg.release_name}

    Summary: {pkg.info.summary}
    Release date: {f"{pkg.upload_time.date()} at {pkg.upload_time.astimezone().timetz()}" if pkg.upload_time else "N/A"}
    Homepage: {pkg.info.home_page}
    PyPI URL: {pkg.info.package_url}
    Documentation: {pkg.info.project_urls.Documentation if hasattr(pkg.info.project_urls, 'Documentation') else "N/A"}
    Author: {pkg.info.author} <{pkg.info.author_email}>
    Maintainer: {pkg.info.maintainer or pkg.info.author} <{pkg.info.maintainer_email or pkg.info.author_email}>
    License: {pkg.info.license}
    Python Version(s): {pkg.info.requires_python or "Not Specified"}
    Dependencies: ({len(pkg.info.requires_dist) if pkg.info.requires_dist else 0}) \n\t\t{indent_chars.join(pkg.info.requires_dist) if pkg.info.requires_dist else ""}
    """
    )
    if pkg.vulnerabilities:
        msg += f"\u001b[1m\u001b[31m\n== WARNING ==\u001b[0m\nThis version has \u001b[1m\u001b[31m{len(pkg.vulnerabilities)}\u001b[0m known security vulnerabilities, use the '--vulnerabilities' flag to view them\n"
    if pkg.info.yanked:
        msg += f"\u001b[1m\u001b[33m\n== NOTE ==\u001b[0m\nThis version has been yanked from PyPI.\n\t Reason: '{pkg.info.yanked_reason}'\n"
    print(msg)
    raise SystemExit(0)
