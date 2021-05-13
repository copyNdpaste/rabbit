from datetime import datetime
from pydantic import BaseModel, StrictInt, StrictStr

from core.domains.region.entity.region_entity import RegionEntity


class UserResponseBaseSchema(BaseModel):
    id: StrictInt = None
    nickname: StrictStr = None
    login_id: str = None
    profile_id: int = None
    status: str = None
    provider: str = None
    region_id: int = None
    created_at: datetime = None
    updated_at: datetime = None
    user_profile: str = None
    region: RegionEntity = None


class UserResponseSchema(BaseModel):
    user: UserResponseBaseSchema = None
