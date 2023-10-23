from requests import get
from logger import logger


class CommunautoClient:
    def __init__(self):
        self.base_url = 'https://restapifrontoffice.reservauto.net/api'

    def getBranches(self, branchId=1) -> dict:
        version = 'v2'
        endpoint = 'AvailableBranch'
        params = {
            'branchId': branchId
        }
        url = f'{self.base_url}/{version}/{endpoint}'
        try:
            response = get(url, params=params)
            return response.json()
        except Exception as e:
            logger.error(e)
            return None



