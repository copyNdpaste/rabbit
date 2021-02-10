from pydantic import BaseModel


class LikePostDto(BaseModel):
    user_id: int
    post_id: int
