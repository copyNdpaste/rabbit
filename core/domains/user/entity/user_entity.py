from datetime import datetime
from pydantic import BaseModel
from core.domains.region.entity.region_entity import RegionEntity


class UserEntity(BaseModel):
    id: int
    login_id: str
    nickname: str
    profile_id: int
    status: str
    provider: str
    region_id: int
    created_at: datetime
    updated_at: datetime
    user_profile: str
    region: RegionEntity
