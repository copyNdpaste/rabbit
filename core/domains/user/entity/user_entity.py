from dataclasses import dataclass
from datetime import datetime


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
