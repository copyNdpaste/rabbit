from datetime import datetime
from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr


class PostReportResponseSchema(BaseModel):
    id: StrictInt = None
    post_id: StrictInt = None
    report_user_id: StrictInt = None
    status: StrictStr = None
    context: StrictStr = None
    confirm_admin_id: Optional[int] = None
    is_system_report: bool = None
    created_at: datetime = None
    updated_at: datetime = None
