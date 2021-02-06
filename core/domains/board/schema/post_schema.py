from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, StrictInt, StrictStr

from core.domains.user.entity.user_entity import UserEntity


class PostResponseBaseSchema(BaseModel):
    id: StrictInt
    user_id: StrictInt
    title: StrictStr
    body: StrictStr
    region_name: StrictStr = None
    region_group_id: StrictInt
    region_group_name: StrictStr
    type: StrictStr
    is_comment_disabled: bool
    is_deleted: bool
    is_blocked: bool
    report_count: StrictInt
    read_count: StrictInt
    category: StrictInt
    last_user_action: StrictStr
    last_user_action_at: Optional[datetime]
    last_admin_action: StrictStr
    last_admin_action_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    user: UserEntity
    post_like_count: StrictInt
    post_like_state: StrictStr


class PostResponseSchema(BaseModel):
    post: PostResponseBaseSchema


class PostListResponseSchema(BaseModel):
    post_list: List[PostResponseBaseSchema]
