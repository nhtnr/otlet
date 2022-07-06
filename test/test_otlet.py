import pytest
from otlet import *

### otlet.api.PackageObject ###

def test_packageobject_call() -> bool:
    pkg = PackageObject("otlet-test-project")
def test_packageobject_fail_nopkg() -> bool:
    with pytest.raises(PyPIPackageNotFound):
        pkg = PackageObject('thispackagedoesnotexistinthepypirepository123456789')
def test_packageobject_fail_noversion() -> bool:
    with pytest.raises(PyPIPackageVersionNotFound):
        pkg = PackageObject("otlet-test-project", "1.0.0")

### otlet.api.PackageInfoObject ###

def test_packageinfoobject_call() -> bool:
    pkg_info = PackageInfoObject("otlet-test-project")
def test_packageinfoobject_reffrompackageobject() -> bool:
    pkg = PackageObject("otlet-test-project")
    pkginfo = pkg.info

### otlet.api.PackageDependencyObject ##

_pdotpkg = PackageObject("otlet-test-project")
def test_packagedependencyobject_populate() -> bool:
    _pdotpkg.dependencies[-1].populate(0)
def test_packagedependencyobject_propertyfail() -> bool:
    with pytest.raises(NotPopulatedError):
        _pdotpkg.dependencies[0].version