import logging
from logging.handlers import TimedRotatingFileHandler
import json
from datetime import datetime
from requests import get

emoji_dict = {
    'DEBUG': '🐛',
    'INFO': '',
    'WARNING': '❗',
    'ERROR': '❌',
    'CRITICAL': '💥',
}
class EmojiFormatter(logging.Formatter):
    def format(self, record):
        level_name = record.levelname
        emoji = emoji_dict.get(level_name, '')
        record.levelname = f'{level_name} {emoji}'
        return super().format(record)

logger = logging.getLogger(__name__)
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.INFO)
log_format = EmojiFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_to_console.setFormatter(log_format)
logger.addHandler(log_to_console)
logger.setLevel(logging.INFO)


class ReservautoClient:
    '''A client to communicate with Reservauto's API.'''
    def __init__(self):
        logger.info('Initializing Reservauto client...')
        self.base_url = 'https://restapifrontoffice.reservauto.net/api'
        self.branches = None
        self.cities = None
        self.stations = None
        logger.info('✅ Reservauto client initialized.')

    def get_branches(self) -> dict:
        '''Returns a list of all available branches.'''

        logger.info('Getting branches...')

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
                    logger.warning(
                        f'Warning {response.status_code} for branch {i}')
                    continue
                for branch in response.json().get('branches'):
                    if branch.get('branchId') == i:
                        branches.append(branch)

            except Exception as e:
                logger.error(e)
                return None

        self.branches = branches
        logger.info(f'✅ Found {len(self.branches)} branches.')
        return self.branches
    

    def get_cities(self, branch_id: int) -> dict:
        '''Returns a list of all available cities for a given branch.'''

        logger.info(f'Getting cities for branch {branch_id}...')

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
            logger.info(f'✅ Found {len(self.cities)} cities.')
            return self.cities

        except Exception as e:
            logger.error(e)
            return None


    def get_stations_availability(self, min_latitude: float, max_latitude: float, min_longitude: float, max_longitude: float, start_datetime: datetime, end_datetime: datetime, city_id: int = None, city: dict = None) -> dict:
        '''Returns a list of all available stations for a given city, location and time range.'''

        logger.info(f'Getting stations for city {city.get("cityLocalizedName")} from {start_datetime} to {end_datetime}...')

        version = 'v2'
        endpoint = 'StationAvailability'

        if city_id is None and city is None:
            logger.error('Error: city_id or city must be specified.')
            return None
        elif city_id is None:
            city_id = city.get('cityId')

        url = f'{self.base_url}/{version}/{endpoint}'
        params = {
            'cityId': city.get('cityId'),
            'MinLatitude': min_latitude,
            'MaxLatitude': max_latitude,
            'MinLongitude': min_longitude,
            'MaxLongitude': max_longitude,
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
            logger.info(f'✅ Found {len(self.stations)} stations.')
            return self.stations

        except Exception as e:
            logger.error(e)
            return None
