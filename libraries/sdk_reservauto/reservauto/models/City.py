from pydantic import BaseModel
from .Location import Location


class City(BaseModel):
    cityId: int
    cityLocalizedName: str
    branchId: int
    isDefaultBranchCity: bool
    cityCenterLocation: Location
