import datetime
import pytest
from reservauto.client import ReservautoClient

saved_branches = ReservautoClient().get_branches()
saved_cities = ReservautoClient().get_cities(branch_id=1)
saved_stations_availability = ReservautoClient().get_stations_availability(
    city=saved_cities[1], 
    min_latitude=45.5, 
    max_latitude=45.6, 
    min_longitude=-73.6,
    max_longitude=-73.5,
    start_datetime=datetime.datetime.now() + datetime.timedelta(weeks=4),
    end_datetime=datetime.datetime.now() + datetime.timedelta(weeks=4, hours=1)
)

@pytest.fixture
def branches():
    return saved_branches

def test_getBranches_type(branches):
    assert isinstance(branches, list)

def test_getBranches_element_type(branches):
    assert isinstance(branches[0], dict)

def test_getBranches_element_keys(branches):
    assert branches[0].keys() == {'branchId', 'branchLocalizedName', 'branchAreaLocalizedName'}


@pytest.fixture
def cities():
    return saved_cities

def test_getCities_type(cities):
    assert isinstance(cities, list)

def test_getCities_element_type(cities):
    assert isinstance(cities[0], dict)

def test_getCities_element_keys(cities):
    assert cities[0].keys() == {'cityId', 'cityLocalizedName', 'branchId', 'isDefaultBranchCity', 'cityCenterLocation'}


@pytest.fixture
def stations_availability():
    return saved_stations_availability

def test_getStationsAvailability_type(stations_availability):
    assert isinstance(stations_availability, list)

def test_getStationsAvailability_element_type(stations_availability):
    assert isinstance(stations_availability[0], dict)

def test_getStationsAvailability_element_keys(stations_availability):
    assert stations_availability[0].keys() == {'stationId', 'stationNb', 'stationName', 'stationLocation', 'cityId', 'recommendedVehicleId', 'hasAllRequestedOptions', 'satisfiesFilters', 'vehiclePromotions', 'hasZone'}
