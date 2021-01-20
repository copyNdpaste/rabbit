from dataclasses import dataclass
from datetime import datetime


@dataclass
class PostReportEntity:
    id: int
    post_id: int
    report_user_id: int
    status: str
    context: str
    confirm_admin_id: int
    is_system_report: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class CommentReportEntity:
    id: int
    comment_id: int
    report_user_id: int
    status: str
    context: str
    confirm_admin_id: int
    is_system_report: bool
    created_at: datetime
    updated_at: datetime
