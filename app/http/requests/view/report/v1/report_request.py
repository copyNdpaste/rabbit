from pydantic import ValidationError
from pydantic import BaseModel

from app.extensions.utils.log_helper import logger
from core.domains.report.dto.post_report_dto import CreatePostReportDto

logger = logger.getLogger(__name__)


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
            schema = CreatePostReportSchema(
                post_id=self.post_id,
                report_user_id=self.report_user_id,
                status=self.status,
                context=self.context,
                confirm_admin_id=self.confirm_admin_id,
                is_system_report=self.is_system_report,
            ).dict()
            return CreatePostReportDto(**schema)
        except ValidationError as e:
            logger.error(
                f"[CreatePostReportRequest][validate_request_and_make_dto] error : {e}"
            )
            return False
