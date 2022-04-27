"""
otlet.types
======================
Classes used by otlet for storing data returned from PyPI Web API.
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

import re
import time
import datetime
from typing import Any, Optional, Dict, List
from types import SimpleNamespace
from dataclasses import dataclass


@dataclass
class PackageInfoObject:
    """
    Contains data from API response key: 'info'

    :param author: Author of the package
    :type author: str

    :param author_email: Email of the package author
    :type author_email: str

    :param bugtrack_url: URL for the package's bug tracker, if available
    :type bugtrack_url: Optional[str]

    :param classifiers: PEP 301 package classifiers
    :type classifiers: List[str]

    :param description: Package description
    :type description: Optional[str]

    :param description_content_type: Type format for package description, if applicable
    :type description_content_type: Optional[str]

    :param docs_url: URL for package's documentation, if available
    :type docs_url: Optional[str]

    :param download_url: Legacy attribute (deprecated)
    :type download_url: Optional[str]

    :param downloads: Legacy attribute (deprecated)
    :type downloads: :class:`types.SimpleNamespace`

    :param home_page: URL for package's home page
    :type home_page: Optional[str]

    :param keywords: Keywords used to help searching for package
    :type keywords: Optional[str]

    :param license: Package license type
    :type license: Optional[str]

    :param maintainer: Maintainer of the package
    :type maintainer: Optional[str]

    :param maintainer_email: Email of the package maintainer
    :type maintainer_email: Optional[str]

    :param name: Package name
    :type name: str

    :param package_url: Main URL for the package
    :type package_url: str

    :param platform: Legacy attribute (deprecated)
    :type platform: Optional[str]

    :param project_url: Main URL for the package
    :type project_url: str

    :param project_urls: Additional relevant URLs for the package
    :type project_urls: Optional[:class:`types.SimpleNamespace`]

    :param release_url: URL for current release version of the package
    :type release_url: str

    :param requires_dist: List of the package's dependencies
    :type requires_dist: Optional[List[str]]

    :param requires_python: Python version constraints
    :type requires_python: Optional[str]

    :param summary: Short summary of the package's function
    :type summary: str

    :param version: Package version (current stable version, if not specified)
    :type version: str

    :param yanked: Whether or not this version has been yanked
    :type yanked: bool

    :param yanked_reason: If this version has been yanked, reason as to why
    :type yanked_reason: Optional[str]
    """

    author: str
    author_email: str
    bugtrack_url: Optional[str]
    classifiers: List[str]
    description: Optional[str]
    description_content_type: Optional[str]
    docs_url: Optional[str]
    download_url: Optional[str]
    downloads: SimpleNamespace
    home_page: Optional[str]
    keywords: Optional[str]
    license: Optional[str]
    maintainer: Optional[str]
    maintainer_email: Optional[str]
    name: str
    package_url: str
    platform: Optional[str]
    project_url: str
    project_urls: Optional[SimpleNamespace]
    release_url: str
    requires_dist: Optional[List[str]]
    requires_python: Optional[str]
    summary: str
    version: str
    yanked: bool
    yanked_reason: Optional[str]

    @classmethod
    def construct(cls, pkginfo: Dict[str, Any]):
        return cls(
            pkginfo["author"],
            pkginfo["author_email"],
            pkginfo["bugtrack_url"],
            pkginfo["classifiers"],
            pkginfo["description"],
            pkginfo["description_content_type"],
            pkginfo["docs_url"],
            pkginfo["download_url"],
            SimpleNamespace(**pkginfo["downloads"]),
            pkginfo["home_page"],
            pkginfo["keywords"],
            pkginfo["license"],
            pkginfo["maintainer"],
            pkginfo["maintainer_email"],
            pkginfo["name"],
            pkginfo["package_url"],
            pkginfo["platform"],
            pkginfo["project_url"],
            SimpleNamespace(**pkginfo["project_urls"])
            if pkginfo["project_urls"]
            else None,
            pkginfo["release_url"],
            pkginfo["requires_dist"],
            pkginfo["requires_python"],
            pkginfo["summary"],
            pkginfo["version"],
            pkginfo["yanked"],
            pkginfo["yanked_reason"],
        )


@dataclass
class URLReleaseObject:
    """
    Contains data from API response key: 'urls'

    :param comment_text: Legacy attribute (deprecated)
    :type comment_text: str

    :param digests: Checksum digests for package release
    :type digests: :class:`types.SimpleNamespace`

    :param downloads: Legacy attribute (deprecated)
    :type downloads: int

    :param filename: Name of the release file
    :type filename: str

    :param has_sig: Presence of PGP signature with release
    :type has_sig: bool

    :param md5_digest: MD5 checksum digest for package release
    :type md5_digest: str

    :param packagetype: Type of package release
    :type packagetype: str

    :param python_version: PEP 425-compliant compatibility tag ('source' if source dist)
    :type python_version: str

    :param size: File size, in bytes
    :type size: int

    :param upload_time: Datetime object for when release was uploaded to PyPI
    :type upload_time: :class:`datetime.datetime`

    :param url: Package release's download URL
    :type url: str

    :param yanked: Whether or not this version has been yanked
    :type yanked: bool

    :param yanked_reason: If this version has been yanked, reason as to why
    :type yanked_reason: Optional[str]
    """

    comment_text: str
    digests: SimpleNamespace
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    size: int
    upload_time: datetime.datetime
    url: str
    yanked: bool
    yanked_reason: Optional[str]

    @classmethod
    def construct(cls, url_release_item: Dict[str, Any]):
        return cls(
            url_release_item["comment_text"],
            SimpleNamespace(**url_release_item["digests"]),
            url_release_item["downloads"],
            url_release_item["filename"],
            url_release_item["has_sig"],
            url_release_item["md5_digest"],
            url_release_item["packagetype"],
            url_release_item["python_version"],
            url_release_item["size"],
            datetime.datetime(
                *time.strptime(
                    url_release_item.get(
                        "upload_time", url_release_item["upload_time_iso_8601"]
                    ),
                    "%Y-%m-%dT%H:%M:%S",
                )[:6]
            ),
            url_release_item["url"],
            url_release_item["yanked"],
            url_release_item["yanked_reason"],
        )


@dataclass
class PackageObject:
    """
    Contains full API response data

    :param info: Info about a given package version
    :type info: :class:`~PackageInfoObject`

    :param last_serial: The most recent serial ID number for the package.
    :type last_serial: int

    :param releases: Dictionary containing all release objects for a given package
    :type releases: Dict[str, :class:`~URLReleaseObject`]

    :param urls: List of package releases for the given version
    :type urls: List[:class:`~URLReleaseObject`]

    :param vulnerabilities: Object containing vulnerability details for the given version, if applicable.
    :type vulnerabilities: Optional[Dict]
    """

    info: PackageInfoObject
    last_serial: int
    releases: Dict[str, URLReleaseObject]
    urls: List[URLReleaseObject]
    vulnerabilities: Optional[Dict]

    @classmethod
    def construct(cls, http_request: Dict[str, Any]):
        j = cls(
            PackageInfoObject.construct(http_request["info"]),
            http_request["last_serial"],
            dict(),
            [URLReleaseObject.construct(x) for x in http_request["urls"]],
            None,
        )
        for k, v in http_request["releases"].items():
            if not v:
                continue
            j.releases[k] = URLReleaseObject.construct(v[0])
        return j

    @property
    def name(self):
        return (
            re.compile(r"[-_.]+").sub("-", self.info.name).lower()
        )  # canonicalize name, stolen from packaging module

    @property
    def version(self):
        return self.info.version

    @property
    def upload_time(self):
        try:
            return self.releases[self.info.version].upload_time
        except KeyError:
            return None


__all__ = ["PackageInfoObject", "URLReleaseObject", "PackageObject"]
