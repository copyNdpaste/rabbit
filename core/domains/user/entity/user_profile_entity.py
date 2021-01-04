from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserProfileEntity:
    id: int
    uuid: str
    file_name: str
    path: str
    created_at: datetime
    updated_at: datetime
