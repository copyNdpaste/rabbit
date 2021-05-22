from datetime import datetime
from pydantic import BaseModel


class UserProfileEntity(BaseModel):
    id: int
    uuid: str
    file_name: str
    path: str
    extension: str
    created_at: datetime
    updated_at: datetime
