# Reservauto API (unofficial)

This is an unofficial package to interact with the official Reservauto API available for testiing with Swagger UI at <https://restapifrontoffice.reservauto.net/ReservautoFrontOffice>

## Installation

```bash
pip install reservauto
```

## Usage

```python
from reservauto import ReservautoClient

client = ReservautoClient()

# Get available branches (already loaded upon initialization)
branches = client.get_branches()

# Get cities for a branch
cities = client.get_cities(branch_id=1)

# Get stations availability for a city, location, and date range
stations_availability = client.get_stations_availability(
    city=cities[1], 
    min_latitude=45.5, 
    max_latitude=45.6, 
    min_longitude=-73.6,
    max_longitute=-73.5,
    start_datetime=datetime.datetime(2021, 1, 1, 12, 0, 0),
    end_datetime=dateetime.datetime(2021, 1, 1, 13, 0, 0),
)
```