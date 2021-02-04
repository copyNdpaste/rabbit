from datetime import datetime
from pydantic import BaseModel


class PostLikeStateEntity(BaseModel):
    id: int
    post_id: int
    user_id: int
    state: str
    created_at: datetime
    updated_at: datetime
