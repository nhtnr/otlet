import sys
from argparse import ArgumentParser
from .arguments import *

if "releases" not in sys.argv:
    ARGUMENT_LIST["package"] = PACKAGE_ARGUMENT
else:
    RELEASES_ARGUMENT_LIST["package"] = PACKAGE_ARGUMENT

class OtletArgumentParser(ArgumentParser):
    def __init__(self):
        super().__init__(
            prog="otlet",
            description="Retrieve information about packages available on PyPI",
            epilog="(c) 2022-present Noah Tanner, released under the terms of the MIT License",
        )
        self.arguments = ARGUMENT_LIST
        self.releases_arguments = RELEASES_ARGUMENT_LIST
        for key, arg in self.arguments.items():
            self.add_argument(*arg["opts"], **self.without_keys(arg, "opts"), dest=key)
        if "releases" in sys.argv or "--help" in sys.argv:
            self.subparsers = self.add_subparsers(parser_class=ArgumentParser)
            self.releases_subparser = self.subparsers.add_parser(
                "releases",
                description="List releases for a specified package", 
                help="List releases for a specified package"
            )
            for key,arg in self.releases_arguments.items():
                self.releases_subparser.add_argument(*arg["opts"], **self.without_keys(arg, "opts"), dest=key)

    def without_keys(self, d, keys):
        return {x: d[x] for x in d if x not in keys}