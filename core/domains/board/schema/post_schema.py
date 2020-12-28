from datetime import datetime

from pydantic import BaseModel, StrictInt, StrictStr


class PostResponseSchema(BaseModel):
    id: StrictInt
    user_id: StrictInt
    title: StrictStr
    region_group_id: StrictStr
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
