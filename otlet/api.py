"""
otlet.api
======================
Functions that call the PyPI Web API.

.. versionchanged:: 0.4.0
    Changed module name from otlet.http to otlet.api
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
from typing import Optional, Tuple, Union
from io import BufferedWriter
from .exceptions import HashDigestMatchError

from .util import deprecated
from .exceptions import *
from .types import *


def _attempt_request(url: str) -> Union[http.client.HTTPResponse, PyPIPackageNotFound]:
    """Attempt request to given URL. Do not use this function directly."""
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


def get_package(package: str, release: Optional[str] = None) -> PackageObject:
    """
    Get full response from PyPI API.

    :param package: Name of package to search for
    :type package: str
    :param release: Release version of package (optional)
    :type release: Optional[str]
    :return: :class:`~otlet.types.PackageObject`

    .. versionchanged:: 0.6.0
        added release as a optional argument, in order to consolidate from 'get_release_full()'
    """
    if release:
        res = _attempt_request(f"https://pypi.org/pypi/{package}/{release}/json")
        if isinstance(res, PyPIPackageNotFound):
            res = _attempt_request(
                f"https://pypi.org/pypi/{package}/json"
            )  # check if plain package is available
            if res:
                raise PyPIPackageVersionNotFound(
                    f"Version {release} not found for package '{package}' in PyPI repository. Please double-check and try again."
                )
    else:
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

    .. deprecated:: 0.6.0
        This function is deprecated and will be removed in version 1.0.0
    """
    deprecated(
        "'get_release_full' is a deprecated function, and will be removed in version 1.0.0"
    )
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
    pkg = get_package(package)
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


def _download(url: str, dest: Union[str, BufferedWriter]) -> Tuple[int, Optional[str]]:
    """Download a binary file from a given URL. Do not use this function directly."""
    # download file and store bytes
    request_obj = request_url(url)
    data = request_obj.read()

    # enforce that we downloaded the correct file, and no corruption took place
    from hashlib import md5

    data_hash = md5(data).hexdigest()
    cloud_hash = request_obj.headers["ETag"].strip('"')
    if data_hash != cloud_hash:
        raise HashDigestMatchError(
            data_hash,
            cloud_hash,
            f'Hashes do not match. (data_hash ("{data_hash}") != cloud_hash ("{cloud_hash}")',
        )

    # write bytes to destination and return
    bw = 0
    if isinstance(dest, str):
        dest = open(dest, "wb")
    with dest as f:
        bw = f.write(data)
    return bw, dest.name


def download_dist(
    package: str,
    release: Optional[str] = None,
    dist_type: str = "bdist_wheel",
    dest: Optional[Union[str, BufferedWriter]] = None,
) -> bool:
    """
    Download a specified package's distribution file.

    :param package: Name of desired package to download
    :type package: str

    :param release: Version of package to download (Default: stable)
    :type release: Optional[str]

    :param dist_type: Type of distribution to download (Default: bdist_wheel)
    :type dist_type: str

    :param dest: Destination for downloaded output file (Default: original filename)
    :type dest: Optional[Union[str, BufferedWriter]]
    """
    if (
        isinstance(dest, BufferedWriter) and dest.mode != "wb"
    ):  # enforce BufferedWriter is in binary mode
        print("If using BufferedWriter for dest, ensure it is opened in 'wb' mode.")
        return False

    # search for package on PyPI
    try:
        pkg = get_package(package, release)
    except (PyPIPackageNotFound, PyPIPackageVersionNotFound) as e:
        print(e.__str__())
        return False

    # search for requested distribution type in pkg.urls
    # and download distribution
    for url in pkg.urls:
        if url.packagetype == dist_type:
            if dest is None:
                dest = url.filename
            s, f = _download(url.url, dest)
            print("Wrote", s, "bytes to", f)
        else:
            print(
                f'Distribution type "{dist_type}" not available for this version of "{package}".'
            )
            return False
    return True


__all__ = [
    "get_package",
    "get_info",
    "get_release_full",
    "get_release_info",
    "download_dist",
]
