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
    
