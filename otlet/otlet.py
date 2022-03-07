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
from argparse import ArgumentParser
from . import __version__
from . import *
from .exceptions import PyPIAPIError

def init_args():
    parser = ArgumentParser(
        prog='otlet',
        epilog='(c) 2022-present Noah Tanner, released under the terms of the MIT License'
    )
    parser.add_argument('package',
                        metavar=('package [VERSION]'),
                        default=[],
                        nargs='*',
                        type=str,
                        help='The package to search for. (version is optional)')
    parser.add_argument('-v', '--version',
                        help='print version information and exit',
                        action='store_true')
    
    args = parser.parse_args()
    if args.version:
        print(textwrap.dedent(f"""
                        otlet v{__version__}
                        (c) 2022-present Noah Tanner, released under the terms of the MIT License"""))
        raise SystemExit(0)
    if not args.package:
        raise SystemExit("Please supply a package to search for: i.e. 'otlet sampleproject'")

    return args

def main():
    args = init_args()
    try:
        if len(args.package) > 1:
            pkginfo = get_release_info(args.package[0], args.package[1])
        else:
            pkginfo = get_info(args.package[0])
    except PyPIAPIError as err:
        raise SystemExit(f"{args.package[0]}: " + err.__str__())

    indent_chars = '\n\t\t'
    print(textwrap.dedent(f'''Info for package {pkginfo.name} v{pkginfo.version}

    Summary: {pkginfo.summary}
    URL: {pkginfo.package_url}
    Author: {pkginfo.author} <{pkginfo.author_email}>
    License: {pkginfo.license}
    Python Version(s): {pkginfo.requires_python if pkginfo.requires_python else "Not Defined"}
    Dependencies: ({len(pkginfo.requires_dist) if pkginfo.requires_dist else 0}) \n\t\t{indent_chars.join(pkginfo.requires_dist) if pkginfo.requires_dist else ""}'''))

    raise SystemExit(0)