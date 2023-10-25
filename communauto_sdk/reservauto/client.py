import logging
import json
from datetime import datetime
from requests import get

logging.basicConfig(level=logging.DEBUG, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ReservautoClient:
    '''A client to communicate with Reservauto's API.'''
    def __init__(self):
        self.base_url = 'https://restapifrontoffice.reservauto.net/api'
        self.branches = None
        self.cities = None
        self.stations = None
        self.get_branches()

    def get_branches(self) -> dict:
        '''Returns a list of all available branches.'''
        version = 'v2'
        endpoint = 'AvailableBranch'

        branches = []
        for i in range(1, 20):
            params = {
                'branchId': i,
            }
            url = f'{self.base_url}/{version}/{endpoint}'

            try:
                response = get(url, params=params, timeout=5)
                if response.status_code != 200:
                    logger.error(
                        f'Error {response.status_code} for branch {i}')
                    continue
                for branch in response.json().get('branches'):
                    if branch.get('branchId') == i:
                        branches.append(branch)

            except Exception as e:
                logger.error(e)
                return None

        self.branches = branches
        return self.branches

    def get_cities(self, branch_id: int) -> dict:
        '''Returns a list of all available cities for a given branch.'''
        version = 'v2'
        endpoint = 'AvailableCity'

        url = f'{self.base_url}/{version}/Branch/{branch_id}/{endpoint}'
        try:
            response = get(url, timeout=5)
            if response.status_code != 200:
                logger.error(
                    f'Error {response.status_code} for branch {branch_id}')
                return None

            cities = response.json().get('cities')
            filtered_cities = [
                city for city in cities if city.get('branchId') == branch_id]
            self.cities = filtered_cities
            return self.cities

        except Exception as e:
            logger.error(e)
            return None

    def get_stations_availability(self, city: dict, min_latitude: float, max_latitude: float, min_longitude: float, max_longitute: float, start_datetime: datetime, end_datetime: datetime) -> dict:
        '''Returns a list of all available stations for a given city, location and time range.'''

        version = 'v2'
        endpoint = 'StationAvailability'

        url = f'{self.base_url}/{version}/{endpoint}'
        params = {
            'cityId': city.get('cityId'),
            'MinLatitude': min_latitude,
            'MaxLatitude': max_latitude,
            'MinLongitude': min_longitude,
            'MaxLongitude': max_longitute,
            'StartDate': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'EndDate': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        try:
            response = get(url, params=params, timeout=5)
            if response.status_code != 200:
                logger.error(
                    f'Error {response.status_code} for city {city.get("cityName")}')
                return None

            logger.debug(json.dumps(response.json(),
                    indent=4, ensure_ascii=False))
            stations = response.json().get('stations')
            self.stations = stations
            return self.stations

        except Exception as e:
            logger.error(e)
            return None
