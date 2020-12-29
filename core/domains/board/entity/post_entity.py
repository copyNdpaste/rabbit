from dataclasses import dataclass
from datetime import datetime

from core.domains.user.entity.user_entity import UserEntity


@dataclass
class PostEntity:
    id: int
    user_id: int
    title: str
    region_group_id: str
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
