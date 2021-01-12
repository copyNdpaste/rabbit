from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReportEntity:
    id: int
    ref_id: int
    type: str
    report_user_id: int
    status: str
    context: str
    confirm_admin_id: int
    is_system_report: bool
    created_at: datetime
    updated_at: datetime
