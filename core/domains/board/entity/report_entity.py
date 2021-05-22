from datetime import datetime
from pydantic import BaseModel


class PostReportEntity(BaseModel):
    id: int
    post_id: int
    report_user_id: int
    status: str
    context: str
    confirm_admin_id: int = None
    is_system_report: bool
    created_at: datetime
    updated_at: datetime


class CommentReportEntity(BaseModel):
    id: int
    comment_id: int
    report_user_id: int
    status: str
    context: str
    confirm_admin_id: int = None
    is_system_report: bool
    created_at: datetime
    updated_at: datetime
