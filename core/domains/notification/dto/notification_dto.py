from pydantic import BaseModel


class MessageDto(BaseModel):
    post_id: int
    user_id: int
    category: str
    type: str
    msg: str


class NotificationHistoryDto(BaseModel):
    user_id: int
    category: str
    type: str
    status: str
    message: dict
