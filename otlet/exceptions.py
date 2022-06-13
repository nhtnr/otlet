"""
otlet.exceptions
======================
Custom exceptions used by otlet
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


class PyPIAPIError(Exception):
    """Generic error pertaining to the PyPI API, not an otlet error."""

    def __init__(self, message: str = None) -> None:
        super().__init__(message)


class PyPIPackageNotFound(PyPIAPIError):
    """Raised when a specified package WAS NOT found in the package index."""

    def __init__(self, package) -> None:
        super().__init__(f"Package '{package}' not found in PyPI repository. Please check your spelling and try again.")


class PyPIPackageVersionNotFound(PyPIAPIError):
    """Raised when a specified package WAS found, but the specified version WAS NOT."""

    def __init__(self, package: str, release: str) -> None:
        super().__init__(f"Version {release} not found for package '{package}' in PyPI repository. Please double-check and try again.")


class HashDigestMatchError(Exception):
    """Raised when two hash digests do not match."""

    def __init__(
        self,
        cmp,
        against,
        *args: object,
    ) -> None:
        super().__init__(*args)
        self.cmp = cmp  # hash that was being check
        self.against = against  # hash that 'cmp' was being compared against


__all__ = [
    "PyPIAPIError",
    "PyPIPackageNotFound",
    "PyPIPackageVersionNotFound",
    "HashDigestMatchError",
]
