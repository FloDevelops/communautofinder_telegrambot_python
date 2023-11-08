import datetime
import json
from reservauto.client import ReservautoClient

client = ReservautoClient()

branches = client.get_branches()
cities = client.get_cities(branch_id=1)
stations = client.get_stations_availability(
    city=cities[1], 
    min_latitude=45.5, 
    max_latitude=45.6, 
    min_longitude=-73.6,
    max_longitute=-73.5,
    start_datetime=datetime.datetime.now() + datetime.timedelta(weeks=3),
    end_datetime=datetime.datetime.now() + datetime.timedelta(weeks=3, hours=1)
)

logs = {
    'branches': branches,
    'cities': cities,
    'stations': stations
}

with open(f'logs/{datetime.datetime.now()}.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(logs, indent=4, ensure_ascii=False))
