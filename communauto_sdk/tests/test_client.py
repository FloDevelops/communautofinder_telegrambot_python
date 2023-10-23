import pytest
from communauto_sdk import CommunautoClient


@pytest.fixture
def client():
    return CommunautoClient()