from pydantic import BaseModel


class Branch(BaseModel):
    branchId: int
    branchLocalizedName: str
    branchAreaLocalizedName: str
