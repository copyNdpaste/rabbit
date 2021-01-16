from datetime import datetime
from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr


class PostReportResponseSchema(BaseModel):
    id: StrictInt
    post_id: StrictInt
    report_user_id: StrictInt
    status: StrictStr
    context: StrictStr
    confirm_admin_id: Optional[int]
    is_system_report: bool
    created_at: datetime
    updated_at: datetime
