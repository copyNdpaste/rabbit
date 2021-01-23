from dataclasses import dataclass
from datetime import datetime

from core.domains.board.entity.article_entity import ArticleEntity
from core.domains.user.entity.user_entity import UserEntity
from core.domains.user.entity.user_profile_entity import UserProfileEntity


@dataclass
class PostEntity:
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
    last_user_action: str
    last_user_action_at: datetime
    last_admin_action: str
    last_admin_action_at: datetime
    created_at: datetime
    updated_at: datetime
    user: UserEntity


@dataclass
class PostListEntity:
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
    last_user_action: str
    last_user_action_at: datetime
    last_admin_action: str
    last_admin_action_at: datetime
    created_at: datetime
    updated_at: datetime
    user: UserEntity
    user_profile: UserProfileEntity
    region: str
    region_group: str
