from pydantic.main import BaseModel


class CreatePostDto(BaseModel):
    user_id: int
    title: str
    region_group_id: int
    type: str
    is_comment_disabled: bool
    is_deleted: bool
    is_blocked: bool
    report_count: int
    read_count: int
    category: int
