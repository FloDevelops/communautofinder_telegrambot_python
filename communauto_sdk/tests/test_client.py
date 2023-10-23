import pytest
from communauto_sdk.client import CommunautoClient

saved_branches = CommunautoClient().getBranches()
saved_cities = CommunautoClient().getCities(1)

@pytest.fixture
def branches():
    return saved_branches

def test_getBranches_type(branches):
    assert type(branches) == list

def test_getBranches_element_type(branches):
    assert type(branches[0]) == dict

def test_getBranches_element_keys(branches):
    assert branches[0].keys() == {'branchId', 'branchLocalizedName', 'branchAreaLocalizedName'}


@pytest.fixture
def cities():
    return saved_cities

def test_getCities_type(cities):
    assert type(cities) == list

def test_getCities_element_type(cities):
    assert type(cities[0]) == dict

def test_getCities_element_keys(cities):
    assert cities[0].keys() == {'cityId', 'cityLocalizedName', 'branchId', 'isDefaultBranchCity', 'cityCenterLocation'}