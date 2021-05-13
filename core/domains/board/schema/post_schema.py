from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, StrictInt, StrictStr
from core.domains.user.entity.user_entity import UserEntity


class PostResponseBaseSchema(BaseModel):
    id: StrictInt = None
    user_id: StrictInt = None
    title: StrictStr = None
    body: StrictStr = None
    region_name: StrictStr = None
    region_group_id: StrictInt = None
    region_group_name: StrictStr = None
    type: StrictStr = None
    is_comment_disabled: bool = None
    is_deleted: bool = None
    is_blocked: bool = None
    report_count: StrictInt = None
    read_count: StrictInt = None
    category_ids: List[int] = None
    last_user_action: StrictStr = None
    last_user_action_at: Optional[datetime] = None
    last_admin_action: StrictStr = None
    last_admin_action_at: Optional[datetime] = None
    created_at: datetime = None
    updated_at: datetime = None
    user: UserEntity = None
    post_like_count: StrictInt = None
    post_like_state: Optional[StrictStr] = None
    amount: int = None
    unit: str = None
    price_per_unit: int = None
    status: str = None
    attachments: List = []


class PostResponseSchema(BaseModel):
    post: PostResponseBaseSchema = None


class PostListResponseSchema(BaseModel):
    post_list: List[PostResponseBaseSchema]
