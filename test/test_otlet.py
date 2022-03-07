import pytest
from otlet import *

def test_successful_full_fetch():
    res = get_full('otlet')
    assert isinstance(res, PackageObject)

def test_failed_full_fetch():
    with pytest.raises(PyPIPackageNotFound):
        get_full('thispackagedoesnotexistinthepypirepository123456789')

def test_successful_release_fetch():
    res = get_release_full('otlet', '0.1.1')
    assert isinstance(res, PackageObject)

def test_failed_release_fetch():
    with pytest.raises(PyPIAPIError):
        get_release_full('otlet', '0.1.0')

def test_get_info():
    res = get_info('otlet')
    assert isinstance(res, PackageInfoObject)

def test_get_release_info():
    res = get_release_info('otlet', '0.1.1')
    assert isinstance(res, PackageInfoObject)
