PACKAGE_ARGUMENT = {
    "opts": [],
    "metavar": ("package_name"),
    "nargs": 1,
    "type": str,
    "help": "The name of the package to search for"
}

PACKAGE_VERSION_ARGUMENT = {
        "opts": [],
        "metavar": ("package_version"),
        "default": "stable",
        "nargs": "?",
        "type": str,
        "help": "The version of the package to search for (optional)"
    }

ARGUMENT_LIST = {
    "urls": {
        "opts": ["--urls"],
        "help": "print list of all relevant URLs for package",
        "action": "store_true"
    },
    "vulnerabilities": {
        "opts": ["--vulns", "--vulnerabilities"],
        "help": "print information about known vulnerabilities for package release version",
        "action": "store_true"
    },
    "version": {
        "opts": ["-v", "--version"],
        "help": "print version and exit",
        "action": "store_true"
    }
}

RELEASES_ARGUMENT_LIST = {
    "show_vulnerable": {
        "opts": ["--show-vulnerable"],
        "help": "Not implemented",
        "action": "store_true"
    },
    "before_date": {
        "opts": ["-bd", "--before-date"],
        "metavar": ("DATE"),
        "help": "Return releases before specified date",
        "nargs": 1,
        "action": "store"
    },
    "after_date": {
        "opts": ["-ad", "--after-date"],
        "metavar": ("DATE"),
        "help": "Return releases after specified date",
        "nargs": 1,
        "action": "store"
    },
    "before_version": {
        "opts": ["-bv", "--before-version"],
        "metavar": ("VERSION"),
        "help": "Return releases before specified version",
        "nargs": 1,
        "action": "store"
    },
    "after_version": {
        "opts": ["-av", "--after-version"],
        "metavar": ("VERSION"),
        "help": "Return releases after specified version",
        "nargs": 1,
        "action": "store"
    },
}