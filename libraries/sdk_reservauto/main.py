import datetime
import json
from reservauto.client import (
    AvailableBranches,
    ReservautoCities,
    StationAvailability,
    FreeFloatingVehiclesAvailability,
)

branches = AvailableBranches().list()
cities = ReservautoCities(branch_id=1).list()
stations = StationAvailability().list(
    city_id=59,
    min_latitude=45.5,
    max_latitude=45.6,
    min_longitude=-73.6,
    max_longitude=-73.5,
    start_datetime=datetime.datetime.now() + datetime.timedelta(weeks=3),
    end_datetime=datetime.datetime.now() + datetime.timedelta(weeks=3, hours=1),
)
freeFloatingVehicles = FreeFloatingVehiclesAvailability().list(
    city_id=59,
    min_latitude=45.5,
    max_latitude=45.6,
    min_longitude=-73.6,
    max_longitude=-73.5,
)


logs = {
    "branches": branches,
    "cities": cities,
    "stations": stations,
    "freeFloatingVehicles": freeFloatingVehicles,
}

with open(f"logs/{datetime.datetime.now()}.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(logs, indent=4, ensure_ascii=False))
