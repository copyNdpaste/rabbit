from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.domains.board.entity.article_entity import ArticleEntity
from core.domains.region.entity.region_entity import RegionEntity
from core.domains.region.entity.region_group_entity import RegionGroupEntity
from core.domains.user.entity.user_entity import UserEntity
from core.domains.user.entity.user_profile_entity import UserProfileEntity


class PostEntity(BaseModel):
    id: int
    user_id: int
    title: str
    article: ArticleEntity
    region_group_id: int
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


class PostListEntity(BaseModel):
    id: int
    user_id: int
    title: str
    article: ArticleEntity
    region_group_id: int
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
    region: Optional[RegionEntity] = None
    region_group: Optional[RegionGroupEntity] = None
