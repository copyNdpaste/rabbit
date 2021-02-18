from typing import List

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
    amount: int
    unit: str
    price_per_unit: int
    status: str
    category_ids: List[int]


class GetPostListDto(BaseModel):
    region_group_id: int
    previous_post_id: int = None
    title: str = None
    type: str = None
    category_ids: List[int]
    status: str = None


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
    amount: int
    unit: str
    price_per_unit: int
    status: str


class DeletePostDto(BaseModel):
    post_id: int
    user_id: int


class GetSellingPostDto(BaseModel):
    user_id: int
    previous_post_id: int = None
