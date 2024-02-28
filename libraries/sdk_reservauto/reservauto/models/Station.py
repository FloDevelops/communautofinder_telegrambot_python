from pydantic import BaseModel
from .Location import Location


class BaseStation(BaseModel):
    stationId: int
    stationNb: str
    stationName: str
    cityId: int
    hasZone: bool


class Station(BaseStation):
    location: Location
    stationStatus: str


class StationAvailability(BaseStation):
    stationLocation: Location
    recommendedVehicleId: int
    satisfiesFilters: bool
    hasAllRequestedOptions: bool
    vehiclePromotions: list[int] | None
