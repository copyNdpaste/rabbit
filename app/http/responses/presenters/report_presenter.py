from typing import Union

from pydantic import ValidationError

from app.extensions.utils.log_helper import logger_
from app.http.responses import failure_response, success_response
from core.domains.report.schema.post_schema import PostReportResponseSchema
from core.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput, FailureType

logger = logger_.getLogger(__name__)


class PostReportPresenter:
    def transform(self, output: Union[UseCaseSuccessOutput, UseCaseFailureOutput]):
        if isinstance(output, UseCaseSuccessOutput):
            v = output.value
            try:
                schema = PostReportResponseSchema(
                    id=v.id,
                    post_id=v.post_id,
                    report_user_id=v.report_user_id,
                    status=v.status,
                    context=v.context,
                    confirm_admin_id=v.confirm_admin_id,
                    is_system_report=v.is_system_report,
                    created_at=v.created_at,
                    updated_at=v.updated_at,
                )
            except ValidationError as e:
                logger.error(f"[AuthenticationPresenter][transform] error : {e}")
                return failure_response(
                    UseCaseFailureOutput(
                        type=FailureType.SYSTEM_ERROR,
                        message="response schema validation error",
                    )
                )
            result = {
                "data": {"post_report": schema.dict()},
                "meta": {"cursor": output.meta},
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)
