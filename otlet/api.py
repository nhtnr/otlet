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


from urllib.request import urlopen
from typing import BinaryIO, Optional, Tuple, Union
from io import BufferedWriter
from .exceptions import HashDigestMatchError

from .exceptions import *
from .types import *

def _download(url: str, dest: Union[str, BinaryIO]) -> Tuple[int, Optional[str]]:
    """Download a binary file from a given URL. Do not use this function directly."""
    # download file and store bytes
    request_obj = urlopen(url)
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
    dest: Optional[Union[str, BinaryIO]] = None,
) -> bool:
    """
    Download a specified package's distribution file.

    :param package: Name of desired package to download
    :type package: str

    :param release: Version of package to download (Default: stable)
    :type release: Optional[str]

    :param dist_type: Type of distribution to download (Default: bdist_wheel)
    :type dist_type: str

    :param dest: Destination for downloaded output file (Default: current directory with original filename)
    :type dest: Optional[Union[str, BinaryIO]]
    """
    if (
        isinstance(dest, BufferedWriter) and dest.mode != "wb"
    ):  # enforce BufferedWriter is in binary mode
        print("If using BufferedWriter for dest, ensure it is opened in 'wb' mode.")
        return False

    # search for package on PyPI
    try:
        pkg = PackageObject(package, release)
    except (PyPIPackageNotFound, PyPIPackageVersionNotFound) as e:
        print(e.__str__())
        return False

    # search for requested distribution type in pkg.urls
    # and download distribution
    success = False
    for url in pkg.urls:
        if url.packagetype == dist_type:
            if dest is None:
                dest = url.filename
            s, f = _download(url.url, dest)
            print("Wrote", s, "bytes to", f)
            success = True
            break
    if not success:
        print(
            f'Distribution type "{dist_type}" not available for this version of "{package}".'
        )
    return success


__all__ = [
    "download_dist",
]
