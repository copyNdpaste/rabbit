from pydantic import BaseModel


class MessageDto(BaseModel):
    token: str
    post_id: int
    user_id: int
    category: str
    type: str
    title: str
    body: str


class NotificationHistoryDto(BaseModel):
    user_id: int
    category: str
    type: str
    status: str
    message: dict


class KeywordTargetUserDto(BaseModel):
    user_id: int
    category: str
    type: str
    status: str
    message: dict
