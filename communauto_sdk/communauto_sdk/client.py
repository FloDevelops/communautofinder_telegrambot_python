from requests import get
import logging, json

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CommunautoClient:
    def __init__(self):
        self.base_url = 'https://restapifrontoffice.reservauto.net/api'

    def getBranches(self) -> dict:
        version = 'v2'
        endpoint = 'AvailableBranch'

        branches = []
        for i in range(1, 20):
            params = {
                'branchId': i,
            }
            url = f'{self.base_url}/{version}/{endpoint}'

            try:
                response = get(url, params=params)
                if response.status_code != 200:
                    logger.error(f'Error {response.status_code} for branch {i}')
                    continue
                for branch in response.json().get('branches'):
                    if branch.get('branchId') == i:
                        branches.append(branch)

            except Exception as e:
                logger.error(e)
                return None
        
        self.branches = branches
        return self.branches
    
    def getCities(self, branchId: int) -> dict:
        version = 'v2'
        endpoint = 'AvailableCity'

        url = f'{self.base_url}/{version}/Branch/{branchId}/{endpoint}'
        try:
            response = get(url)
            if response.status_code != 200:
                logger.error(f'Error {response.status_code} for branch {branchId}')
                return None
            
            cities = response.json().get('cities')
            filtered_cities = [city for city in cities if city.get('branchId') == branchId]
            self.cities = filtered_cities
            return self.cities
        
        except Exception as e:
            logger.error(e)
            return None
        
    def getStationsAvailability(self, city: dict) -> dict:
        version = 'v2'
        endpoint = 'AvailableCity'

        url = f'{self.base_url}/{version}/Branch/{city.get("branchId")}/{endpoint}'
        params = {
            'cityId': city.get('cityId'),
            'MinLatitude': city.get('isDefaultBranchCity'),
            'MaxLatitude': city.get('cityCenterLocation'),
            'MinLongitude': city.get('cityCenterLocation'),
            'MaxLongitude': city.get('cityCenterLocation'),
            'StartDateTime': '2021-09-01T00:00:00',
            'EndDateTime': '2021-09-01T23:59:59',
        }
        # ...