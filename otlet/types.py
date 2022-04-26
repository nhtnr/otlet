"""
otlet.types - types used by otlet for carrying API response data
CLI tool and wrapper for PyPI JSON Web API

Copyright (c) 2022 Noah Tanner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""

import time
import datetime
from distutils.command.upload import upload
from typing import Any, Optional, Dict, List
from types import SimpleNamespace
from dataclasses import dataclass


@dataclass
class PackageInfoObject:
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
    info: PackageInfoObject
    last_serial: int
    releases: Dict[str, URLReleaseObject]
    urls: List[URLReleaseObject]
    vulnerabilities: Optional[List]

    @classmethod
    def construct(cls, http_request: Dict[str, Any]):
        j = cls(
            PackageInfoObject.construct(http_request["info"]),
            http_request["last_serial"],
            dict(),
            [URLReleaseObject.construct(x) for x in http_request["urls"]],
            http_request["vulnerabilities"],
        )
        for k, v in http_request["releases"].items():
            if not v:
                continue
            j.releases[k] = URLReleaseObject.construct(v[0])
        return j

    @property
    def upload_time(self):
        try:
            return self.releases[self.info.version].upload_time
        except KeyError:
            return None


__all__ = ["PackageInfoObject", "URLReleaseObject", "PackageObject"]
