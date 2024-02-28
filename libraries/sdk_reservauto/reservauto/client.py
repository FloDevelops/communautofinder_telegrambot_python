# import logging
from datetime import datetime
from typing import List, Any, Optional
from requests import get, post, put, delete
from .models.Branch import Branch
from .models.City import City
from .models.Station import StationAvailability as StationAvailabilityModel

# emoji_dict = {
#     "DEBUG": "🐛",
#     "INFO": "",
#     "WARNING": "❗",
#     "ERROR": "❌",
#     "CRITICAL": "💥",
# }

# class EmojiFormatter(logging.Formatter):
#     def format(self, record: logging.LogRecord) -> str:
#         level_name = record.levelname
#         emoji = emoji_dict.get(level_name, "")
#         record.levelname = f"{level_name} {emoji}"
#         return super().format(record)


# logger = logging.getLogger(__name__)
# log_to_console = logging.StreamHandler()
# log_to_console.setLevel(logging.INFO)
# log_format = EmojiFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# log_to_console.setFormatter(log_format)
# logger.addHandler(log_to_console)
# logger.setLevel(logging.INFO)


class BaseReservautoClient:
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://restapifrontoffice.reservauto.net/api"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        version: str = "v2",
    ) -> dict[str, Any]:
        response = get(
            f"{self.base_url}/{version}/{endpoint}",
            headers=self.headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def _post(
        self, endpoint: str, data: dict[str, Any], version: str = "v2"
    ) -> dict[str, Any]:
        response = post(
            f"{self.base_url}/{version}/{endpoint}",
            headers=self.headers,
            json=data,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def _put(
        self, endpoint: str, data: dict[str, Any], version: str = "v2"
    ) -> dict[str, Any]:
        response = put(
            f"{self.base_url}/{version}/{endpoint}",
            headers=self.headers,
            json=data,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def _delete(
        self, endpoint: str, data: dict[str, Any], version: str = "v2"
    ) -> dict[str, Any]:
        response = delete(
            f"{self.base_url}/{version}/{endpoint}",
            headers=self.headers,
            json=data,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()


class AvailableBranches(BaseReservautoClient):
    def __init__(self) -> None:
        super().__init__()
        self.version = "v2"
        self.endpoint = "AvailableBranch"

    def get(self, branch_id: int) -> Optional[Branch]:
        response_body = self._get(
            self.endpoint, params={"branchId": branch_id}, version=self.version
        )
        branches = response_body.get("branches")
        if not branches:
            return None
        branch = next(
            (branch for branch in branches if branch.get("branchId") == branch_id), None
        )
        return branch

    def list(
        self,
    ) -> List[Optional[Branch]]:  # Assuming Branch is a class in the Branch module
        branches: List[Optional[Branch]] = []
        for i in range(1, 15):
            branch: Optional[Branch] = self.get(i)
            if branch is not None:
                branches.append(branch)
        return branches


class ReservautoCities(BaseReservautoClient):
    def __init__(self, branch_id: int) -> None:
        super().__init__()
        self.version = "v2"
        self.endpoint = f"Branch/{branch_id}/AvailableCity"

    def list(self) -> Optional[List[City]]:
        response_body = self._get(self.endpoint, version=self.version)
        return response_body.get("cities")


class StationAvailability(BaseReservautoClient):
    def __init__(self) -> None:
        super().__init__()
        self.version = "v2"
        self.endpoint = "StationAvailability"

    def list(
        self,
        city_id: int,
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> Optional[List[StationAvailabilityModel]]:
        self.city_id = city_id
        self.min_latitude = min_latitude
        self.max_latitude = max_latitude
        self.min_longitude = min_longitude
        self.max_longitude = max_longitude
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        params = {
            "cityId": self.city_id,
            "MinLatitude": self.min_latitude,
            "MaxLatitude": self.max_latitude,
            "MinLongitude": self.min_longitude,
            "MaxLongitude": self.max_longitude,
            "StartDate": self.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "EndDate": self.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        response_body = self._get(self.endpoint, params=params, version=self.version)
        return response_body.get("stations")


class FreeFloatingVehiclesAvailability(BaseReservautoClient):
    def __init__(self) -> None:
        super().__init__()
        self.version = "v2"
        self.endpoint = "Vehicle/FreeFloatingAvailability"

    def list(
        self,
        city_id: int,
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
    ) -> Optional[List[dict[str, Any]]]:
        self.city_id = city_id
        self.min_latitude = min_latitude
        self.max_latitude = max_latitude
        self.min_longitude = min_longitude
        self.max_longitude = max_longitude
        params = {
            "cityId": self.city_id,
            "MinLatitude": self.min_latitude,
            "MaxLatitude": self.max_latitude,
            "MinLongitude": self.min_longitude,
            "MaxLongitude": self.max_longitude,
        }
        response_body = self._get(self.endpoint, params=params, version=self.version)
        return response_body.get("vehicles")
    