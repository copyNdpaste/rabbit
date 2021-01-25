from pydantic import BaseModel


class CreatePostReportDto(BaseModel):
    post_id: int
    report_user_id: int
    status: str
    context: str
    confirm_admin_id: int = None
    is_system_report: bool
