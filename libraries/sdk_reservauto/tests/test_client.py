import datetime
import pytest
from typing import List
from reservauto.client import AvailableBranches, ReservautoCities, StationAvailability
from reservauto.models.Branch import Branch as BranchModel
from reservauto.models.City import City as CityModel
from reservauto.models.Station import StationAvailability as StationAvailabilityModel

saved_branches = AvailableBranches().list()
saved_cities = ReservautoCities(branch_id=1).list()
saved_stations_availability = StationAvailability().list(
    city_id=59,
    min_latitude=45.5,
    max_latitude=45.6,
    min_longitude=-73.6,
    max_longitude=-73.5,
    start_datetime=datetime.datetime.now() + datetime.timedelta(weeks=4),
    end_datetime=datetime.datetime.now() + datetime.timedelta(weeks=4, hours=1),
)


@pytest.fixture
def branches():
    return saved_branches


def test_getBranches_type(branches):
    assert isinstance(branches, list)


def test_getBranches_element_type(branches):
    assert isinstance(branches[0], dict)


def test_getBranches_element_keys(branches):
    assert branches[0].keys() == BranchModel.model_fields.keys()


@pytest.fixture
def cities():
    return saved_cities


def test_getCities_type(cities):
    assert isinstance(cities, list)


def test_getCities_element_type(cities):
    assert isinstance(cities[0], dict)


def test_getCities_element_keys(cities):
    assert cities[0].keys() == CityModel.model_fields.keys()


@pytest.fixture
def stations_availability():
    return saved_stations_availability


def test_getStationsAvailability_type(stations_availability):
    assert isinstance(stations_availability, list)


def test_getStationsAvailability_element_type(stations_availability):
    assert isinstance(stations_availability[0], dict)


def test_getStationsAvailability_element_keys(stations_availability):
    assert (
        stations_availability[0].keys() == StationAvailabilityModel.model_fields.keys()
    )
