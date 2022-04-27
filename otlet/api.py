"""
otlet.api
======================
Functions that call the PyPI Web API.
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


import json
import http.client
from urllib.request import urlopen as request_url
from urllib.error import HTTPError
from typing import Union

from .util import deprecated
from .exceptions import *
from .types import *


def _attempt_request(url: str) -> Union[http.client.HTTPResponse, PyPIPackageNotFound]:
    """Attempt request to given URL. Do not use this function."""
    try:
        res = request_url(url)
    except HTTPError as err:
        if err.code == 404:
            return PyPIPackageNotFound(
                "Package not found in PyPI repository. Please check your spelling and try again."
            )
        else:
            raise err
    return res


def get_full(package: str) -> PackageObject:
    """
    Get full response from PyPI API.

    :param package: Name of package to search for
    :return: :class:`~otlet.types.PackageObject`
    """
    res = _attempt_request(f"https://pypi.org/pypi/{package}/json")
    if isinstance(res, PyPIPackageNotFound):
        raise res
    return PackageObject.construct(json.loads(res.readlines()[0].decode()))


def get_release_full(package: str, release: str) -> PackageObject:
    """
    Get full response from PyPI API for specific version.

    :param package: Name of package to search for
    :param release: Release version of package
    :return: :class:`~otlet.types.PackageObject`
    """
    res = _attempt_request(f"https://pypi.org/pypi/{package}/{release}/json")
    if isinstance(res, PyPIPackageNotFound):
        res = _attempt_request(
            f"https://pypi.org/pypi/{package}/json"
        )  # check if plain package is available
        if isinstance(res, PyPIPackageNotFound):
            raise res  # if not, raise PyPIPackageNotFound
        else:
            raise PyPIPackageVersionNotFound(
                f"Version {release} not found in PyPI repository. Please double-check and try again."
            )
    return PackageObject.construct(json.loads(res.readlines()[0].decode()))


def get_info(package: str) -> PackageInfoObject:
    """
    Get package info from PyPI API.

    :param package: Name of package to search for
    :return: :class:`~otlet.types.PackageInfoObject`

    .. deprecated:: 0.3.0
        This function is deprecated and will be removed in version 1.0.0
    """
    deprecated(
        "get_info and get_release_info are deprecated methods and will be removed in version 1.0.0"
    )
    pkg = get_full(package)
    return pkg.info


def get_release_info(package: str, release: str) -> PackageInfoObject:
    """
    Get package info from PyPI API for specific version.

    :param package: Name of package to search for
    :param release: Release version of package
    :return: :class:`~otlet.types.PackageInfoObject`

    .. deprecated:: 0.3.0
        This function is deprecated and will be removed in version 1.0.0
    """
    pkg = get_release_full(package, release)
    deprecated(
        "get_info and get_release_info are deprecated methods and will be removed in version 1.0.0"
    )
    return pkg.info


__all__ = ["get_full", "get_info", "get_release_full", "get_release_info"]
