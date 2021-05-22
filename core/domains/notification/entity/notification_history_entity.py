from datetime import datetime

from pydantic import BaseModel


class NotificationHistoryEntity(BaseModel):
    id: int
    user_id: int
    notification_id: int
    status: str
    message: str
    created_at: datetime
    updated_at: datetime
