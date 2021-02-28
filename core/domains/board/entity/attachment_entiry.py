from datetime import datetime
from pydantic import BaseModel


class AttachmentEntity(BaseModel):
    id: int
    post_id: int
    type: str
    file_name: str
    path: str
    extension: str
    uuid: str
    created_at: datetime
    updated_at: datetime
