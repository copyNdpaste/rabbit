from datetime import datetime
from pydantic.main import BaseModel


class RegionEntity(BaseModel):
    id: int
    region_group_id: int
    name: str
    created_at: datetime
    updated_at: datetime
