from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.domains.board.enum.post_enum import PostLikeStateEnum
from core.domains.user.entity.user_entity import UserEntity
from core.domains.user.entity.user_profile_entity import UserProfileEntity


class PostEntity(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    region_group_id: int
    region_group_name: str
    type: str
    is_comment_disabled: bool
    is_deleted: bool
    is_blocked: bool
    report_count: int
    read_count: int
    category: int
    last_user_action: Optional[str] = None
    last_user_action_at: Optional[datetime] = None
    last_admin_action: Optional[str] = None
    last_admin_action_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    user: UserEntity
    amount: int
    unit: str
    price_per_unit: int
    status: str
    post_like_count: int = 0
    post_like_state: str = PostLikeStateEnum.DEFAULT.value


class PostListEntity(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    region_name: str
    region_group_id: int
    region_group_name: Optional[str] = None
    type: str
    is_comment_disabled: bool
    is_deleted: bool
    is_blocked: bool
    report_count: int
    read_count: int
    category: int
    last_user_action: Optional[str] = None
    last_user_action_at: Optional[datetime] = None
    last_admin_action: Optional[str] = None
    last_admin_action_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    user: UserEntity
    user_profile: UserProfileEntity
    amount: int
    unit: str
    price_per_unit: int
    status: str
    post_like_count: int = 0
    post_like_state: str = PostLikeStateEnum.DEFAULT.value
