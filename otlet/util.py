from warnings import warn


def deprecated(msg: str = ""):
    warn(msg, DeprecationWarning, 2)
