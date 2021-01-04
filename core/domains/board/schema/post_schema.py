from datetime import datetime

from pydantic import BaseModel, StrictInt, StrictStr

from core.domains.user.entity.user_entity import UserEntity


class PostResponseSchema(BaseModel):
    id: StrictInt
    user_id: StrictInt
    title: StrictStr
    region_group_id: StrictInt
    type: StrictStr
    is_comment_disabled: bool
    is_deleted: bool
    is_blocked: bool
    report_count: StrictInt
    read_count: StrictInt
    category: StrictInt
    last_user_action: StrictStr
    last_user_action_at: datetime
    last_admin_action: StrictStr
    last_admin_action_at: datetime
    created_at: datetime
    updated_at: datetime
    user: UserEntity
