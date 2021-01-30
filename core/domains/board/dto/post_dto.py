from pydantic import BaseModel


class CreatePostDto(BaseModel):
    user_id: int
    title: str
    body: str
    region_group_id: int
    type: str
    is_comment_disabled: bool
    is_deleted: bool
    is_blocked: bool
    report_count: int
    read_count: int
    category: int


class GetPostListDto(BaseModel):
    region_group_id: int
    previous_post_id: int = None
    title: str = None
    type: str = None
    category: str = None


class GetPostDto(BaseModel):
    post_id: int


class UpdatePostDto(BaseModel):
    post_id: int
    user_id: int
    title: str
    body: str
    region_group_id: int
    type: str
    is_comment_disabled: bool
    category: int


class DeletePostDto(BaseModel):
    post_id: int
    user_id: int
