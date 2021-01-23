from datetime import datetime
from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr


class PostResponseSchema(BaseModel):
    id: StrictInt
    user_id: StrictInt
    title: StrictStr
    body: StrictStr
    region_group_id: StrictInt
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
    user_id: StrictInt
    nickname: StrictStr
    login_id: StrictStr
