import pytest
from otlet import *

def test_successful_full_fetch():
    res = get_package('otlet')
    assert isinstance(res, PackageObject)

def test_failed_full_fetch():
    with pytest.raises(PyPIPackageNotFound):
        get_package('thispackagedoesnotexistinthepypirepository123456789')

def test_successful_release_fetch():
    res = get_package('otlet', '0.1.1')
    assert isinstance(res, PackageObject)

def test_failed_release_fetch():
    with pytest.raises(PyPIAPIError):
        get_package('otlet', '0.1.0')
