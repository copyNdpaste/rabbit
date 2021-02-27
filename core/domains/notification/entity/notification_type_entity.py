from pydantic import BaseModel


class NotificationTypeEntity(BaseModel):
    id: int
    category: str
    type: str
