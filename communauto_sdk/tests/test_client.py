import pytest
from communauto_sdk.client import CommunautoClient

branches_testing = CommunautoClient().getBranches()

def test_getBranches_type(branches):
    assert type(branches) == list

def test_getBranches_element_type(branches):
    assert type(branches[0]) == dict

def test_getBranches_element_keys(branches):
    assert branches[0].keys() == {'branchId', 'branchLocalizedName', 'branchAreaLocalizedName'}


