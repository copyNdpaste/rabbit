from pydantic import ValidationError
from pydantic.main import BaseModel

from core.domains.report.dto.post_report_dto import CreatePostReportDto


class CreatePostReportSchema(BaseModel):
    post_id: int
    report_user_id: int
    status: str
    context: str
    confirm_admin_id: int = None
    is_system_report: bool


class CreatePostReportRequest:
    def __init__(
        self,
        post_id,
        report_user_id,
        status,
        context,
        confirm_admin_id,
        is_system_report,
    ):
        self.post_id = post_id
        self.report_user_id = report_user_id
        self.status = status
        self.context = context
        self.confirm_admin_id = confirm_admin_id
        self.is_system_report = is_system_report

    def validate_request_and_make_dto(self):
        try:
            CreatePostReportSchema(
                post_id=self.post_id,
                report_user_id=self.report_user_id,
                status=self.status,
                context=self.context,
                confirm_admin_id=self.confirm_admin_id,
                is_system_report=self.is_system_report,
            )
            return self.to_dto()
        except ValidationError as e:
            # TODO : log로 대체
            print(e)
            return False

    def to_dto(self) -> CreatePostReportDto:
        return CreatePostReportDto(
            post_id=self.post_id,
            report_user_id=self.report_user_id,
            status=self.status,
            context=self.context,
            confirm_admin_id=self.confirm_admin_id,
            is_system_report=self.is_system_report,
        )
