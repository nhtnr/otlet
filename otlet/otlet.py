"""
otlet
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

from http.client import HTTPException
import textwrap
from argparse import ArgumentParser
from . import *

def init_args():
    parser = ArgumentParser(
        prog='otlet',
        epilog='(c) 2022-present Noah Tanner, released under the terms of the MIT License'
    )
    parser.add_argument('package',
                        help='The package to search for.')
    parser.add_argument('version',
                        help='Specific version to get info for. (default: current)',
                        nargs='*',
                        default="")

    return parser.parse_args()

def main():
    args = init_args()
    try:
        if args.version:
            pkginfo = get_release_info(args.package, args.version[0])
        else:
            pkginfo = get_info(args.package)
    except HTTPException as err:
        raise SystemExit(f"{args.package}: " + err.__str__())

    indent_chars = '\n\t\t'
    print(textwrap.dedent(f'''Info for package {pkginfo.name} v{pkginfo.version}

    Summary: {pkginfo.summary}
    URL: {pkginfo.package_url}
    Author: {pkginfo.author} <{pkginfo.author_email}>
    License: {pkginfo.license}
    Python Version(s): {pkginfo.requires_python if pkginfo.requires_python else "Not Defined"}
    Dependencies: ({len(pkginfo.requires_dist) if pkginfo.requires_dist else 0}) \n\t\t{indent_chars.join(pkginfo.requires_dist) if pkginfo.requires_dist else ""}'''))

    raise SystemExit(0)