from datetime import datetime
from pydantic import BaseModel


class RegionGroupEntity(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
