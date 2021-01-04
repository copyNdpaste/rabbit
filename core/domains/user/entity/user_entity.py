from dataclasses import dataclass
from datetime import datetime

from core.domains.region.entity.region_entity import RegionEntity
from core.domains.user.entity.user_profile_entity import UserProfileEntity


@dataclass
class UserEntity:
    id: int
    login_id: str
    nickname: str
    profile_id: int
    status: str
    provider: str
    region_id: int
    created_at: datetime
    updated_at: datetime
    user_profile: UserProfileEntity
    region: RegionEntity
