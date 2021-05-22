from pydantic import ValidationError

from app.extensions.utils.log_helper import logger_
from app.http.responses import failure_response, success_response
from core.domains.authentication.schema.authentication import (
    AuthenticationResponseSchema,
)
from core.use_case_output import UseCaseSuccessOutput, FailureType, UseCaseFailureOutput

logger = logger_.getLogger(__name__)


class AuthenticationPresenter:
    def transform(
        self, response: UseCaseSuccessOutput,
    ):
        try:
            schema = AuthenticationResponseSchema(type=response.type)
        except ValidationError as e:
            logger.error(f"[AuthenticationPresenter][transform] error : {e}")
            return failure_response(
                UseCaseFailureOutput(
                    type=FailureType.SYSTEM_ERROR,
                    message="response schema validation error",
                )
            )
        result = {
            "data": {"result": schema.dict()},
            "meta": {"cursor": response.meta},
        }
        return success_response(result=result)
