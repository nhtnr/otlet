"""
otlet.api
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
import json
from http.client import HTTPResponse
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Any, Optional, Dict, List
from types import SimpleNamespace
from dataclasses import dataclass
from .packaging.version import parse
from .exceptions import PyPIPackageNotFound, PyPIPackageVersionNotFound


class PackageBase(object):
    """
    Base for :class:`~PackageObject` and :class:`~PackageInfoObject`. Should not be directly instantiated.
    """
    def __init__(self, package_name: str, release: Optional[str] = None) -> None:
        self.name = package_name
        self.release = release
        self._http_response = self._attempt_request()
        self.http_response = json.loads(self._http_response.readlines()[0].decode())

    def _attempt_request(self) -> HTTPResponse:
        """Attempt PyPI API request for package. You should not need to call this function directly."""
        try:
            if self.release is None:
                res = urlopen(f"https://pypi.org/pypi/{self.name}/json")
            else:
                res = urlopen(f"https://pypi.org/pypi/{self.name}/{self.release}/json")
        except HTTPError as err:
            if err.code == 404:
                if self.release is None:
                    raise PyPIPackageNotFound(self.name)
                raise PyPIPackageVersionNotFound(self.name, self.release)
            else:
                raise err
        return res

class PackageInfoObject(PackageBase):
    """
    Contains data from API response key: 'info'

    :param package_name: Name of PyPI package to query
    :type package_name: str

    :param release: Specific version to query (optional)
    :type release: str

    :param perform_request: Whether or not to perform a fresh API request upon instantiation
    :type perform_request: bool

    :param http_response: JSON-parsed HTTP Response to be used to populate object (optional)
    :type http_response: Dict[str, Any]

    :var author: Author of the package
    :vartype author: str

    :var author_email: Email of the package author
    :vartype author_email: str

    :var bugtrack_url: Legacy attribute (deprecated) (Use project_urls.Tracker instead)
    :vartype bugtrack_url: Optional[str]

    :var classifiers: PEP 301 package classifiers
    :vartype classifiers: List[str]

    :var description: Package description
    :vartype description: Optional[str]

    :var description_content_type: Type format for package description, if applicable
    :vartype description_content_type: Optional[str]

    :var docs_url: Legacy attribute (deprecated) (Use project_urls.Documentation instead)
    :vartype docs_url: Optional[str]

    :var download_url: Legacy attribute (deprecated)
    :vartype download_url: Optional[str]

    :var downloads: Legacy attribute (deprecated)
    :vartype downloads: :class:`types.SimpleNamespace`

    :var home_page: URL for package's home page
    :vartype home_page: Optional[str]

    :var keywords: Keywords used to help searching for package
    :vartype keywords: Optional[str]

    :var license: Package license type
    :vartype license: Optional[str]

    :var maintainer: Maintainer of the package
    :vartype maintainer: Optional[str]

    :var maintainer_email: Email of the package maintainer
    :vartype maintainer_email: Optional[str]

    :var name: Package name
    :vartype name: str

    :var package_url: Main URL for the package
    :vartype package_url: str

    :var platform: Legacy attribute (deprecated)
    :vartype platform: Optional[str]

    :var project_url: Main URL for the package
    :vartype project_url: str

    :var project_urls: Additional relevant URLs for the package
    :vartype project_urls: Optional[:class:`types.SimpleNamespace`]

    :var release_url: URL for current release version of the package
    :vartype release_url: str

    :var requires_dist: List of the package's dependencies
    :vartype requires_dist: Optional[List[str]]

    :var requires_python: Python version constraints
    :vartype requires_python: Optional[str]

    :var summary: Short summary of the package's function
    :vartype summary: Optional[str]

    :var version: Package version (current stable version, if not specified)
    :vartype version: Union[:class:`packaging.version.Version`, :class:`packaging.version.LegacyVersion`]

    :var yanked: Whether or not this version has been yanked
    :vartype yanked: bool

    :var yanked_reason: If this version has been yanked, reason as to why
    :vartype yanked_reason: str
    """

    def __init__(
        self, 
        package_name: str, 
        release: Optional[str] = None, 
        perform_request: bool = True, 
        http_response: Dict[str, Any] = None
    ) -> None:
        if perform_request:
            super().__init__(package_name, release)
        else:
            self.http_response = http_response

        for k,v in self.http_response["info"].items():
            if v == "":
                self.__dict__[k] = None
            elif k == "downloads" or k == "project_urls":
                self.__dict__[k] = SimpleNamespace(**v) if v else None
            elif k == "version":
                self.__dict__[k] = parse(v)
            self.__dict__[k] = v


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
            url_release_item["yanked_reason"] or None,
        )


@dataclass
class PackageVulnerabilitiesObject:
    """
    Contains information about applicable package vulnerabilities, mainly sourced from 'https://osv.dev/'

    :param aliases: Alias name(s) for this vulnerability, usually a 'CVE-ID'
    :type aliases: List[str]

    :param details: Details about the vulnerability
    :type details: str

    :param fixed_in: Version(s) that the vulnerability was patched in
    :type fixed_in: List[str]

    :param id: 'PYSEC-ID' for this vulnerability
    :type id: str

    :param link: Link to web page where this information was sourced from, usually an 'https://osv.dev/' link
    :type link: str

    :param source: Where this vulnerability information was sourced from, usually 'osv'
    :type source: str

    .. versionadded:: 0.4.0
    """

    aliases: List[str]
    details: str
    fixed_in: List[str]
    id: str
    link: str
    source: str

    @classmethod
    def construct(cls, vuln_dict: Dict[str, Any]):
        return cls(
            vuln_dict["aliases"],
            vuln_dict["details"],
            vuln_dict["fixed_in"],
            vuln_dict["id"],
            vuln_dict["link"],
            vuln_dict["source"],
        )

class PackageObject(PackageBase):
    """
    Contains full API response data

    :param package_name: Name of PyPI package to query
    :type package_name: str

    :param release: Specific version to query (optional)
    :type release: str

    :var info: Info about a given package version
    :vartype info: :class:`~PackageInfoObject`

    :var last_serial: The most recent serial ID number for the package.
    :vartype last_serial: int

    :var releases: Dictionary containing all release objects for a given package
    :vartype releases: Dict[Union[:class:`packaging.version.Version`, :class:`packaging.version.LegacyVersion`], :class:`~URLReleaseObject`]

    :var urls: List of package releases for the given version
    :vartype urls: List[:class:`~URLReleaseObject`]

    :var vulnerabilities: List of objects containing vulnerability details for the given version, if applicable.
    :vartype vulnerabilities: Optional[List[:class:`~PackageVulnerabilitiesObject`]]
    """

    def __init__(self, package_name: str, release: Optional[str] = None) -> None:
        super().__init__(package_name, release)
        self.info = PackageInfoObject(package_name, release, False, self.http_response)
        self.last_serial = self.http_response["last_serial"]
        self.releases = dict()
        self.urls = [URLReleaseObject.construct(_) for _ in self.http_response["urls"]]
        self.vulnerabilities = [
                PackageVulnerabilitiesObject.construct(_)
                for _ in self.http_response["vulnerabilities"]
            ] or None

        for k, v in self.http_response["releases"].items():
            if not v:
                continue
            self.releases[parse(k)] = URLReleaseObject.construct(v[0])

    @property
    def canonicalized_name(self):
        return (
            re.compile(r"[-_.]+").sub("-", self.info.name).lower()
        )  # stolen from packaging module

    @property
    def version(self):
        return self.info.version.__str__()

    @property
    def release_name(self):
        return f"{self.name} v{self.version}"

    @property
    def upload_time(self):
        try:
            return self.releases[self.info.version].upload_time
        except KeyError:
            return None


__all__ = [
    "PackageInfoObject",
    "URLReleaseObject",
    "PackageObject",
    "PackageVulnerabilitiesObject",
]
