from warnings import warn


def deprecated(msg: str = ""):
    """Print DeprecationWarning with given text."""
    warn(msg, DeprecationWarning, 2)
