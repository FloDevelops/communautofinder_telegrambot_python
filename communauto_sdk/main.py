# import json, datetime
from reservauto.client import ReservautoClient

client = ReservautoClient()
# branches = client.get_branches()
# print(type(branches))
# print(branches)
# print(json.dumps(branches, indent=4, ensure_ascii=False))

# print(json.dumps(client.get_cities(branch_id=1), indent=4, ensure_ascii=False))

# print(json.dumps(
#     client.get_stations_availability(
#         city=client.get_cities(branch_id=1)[1], 
#         min_latitude=45.5, 
#         max_latitude=45.6, 
#         min_longitude=-73.6,
#         max_longitute=-73.5,
#         start_datetime=datetime.datetime.now() + datetime.timedelta(weeks=3),
#         end_datetime=datetime.datetime.now() + datetime.timedelta(weeks=3, hours=1)
#     ), 
#     indent=4, ensure_ascii=False))