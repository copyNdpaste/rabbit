from datetime import datetime
from pydantic import BaseModel, StrictInt, StrictStr

from core.domains.region.entity.region_entity import RegionEntity


class UserResponseBaseSchema(BaseModel):
    id: StrictInt
    nickname: StrictStr
    login_id: str
    profile_id: int
    status: str
    provider: str
    region_id: int
    created_at: datetime
    updated_at: datetime
    user_profile: str
    region: RegionEntity


class UserResponseSchema(BaseModel):
    user: UserResponseBaseSchema
