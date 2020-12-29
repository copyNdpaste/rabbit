from typing import Union

from pydantic import ValidationError

from app.http.responses import failure_response, success_response
from core.domains.board.schema.post_schema import PostResponseSchema
from core.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput, FailureType


class PostPresenter:
    def transform(self, output: Union[UseCaseSuccessOutput, UseCaseFailureOutput]):
        if isinstance(output, UseCaseSuccessOutput):
            value = output.value
            try:
                schema = PostResponseSchema(
                    id=value.id,
                    user_id=value.user_id,
                    title=value.title,
                    region_group_id=value.region_group_id,
                    type=value.type,
                    is_comment_disabled=value.is_comment_disabled,
                    is_deleted=value.is_deleted,
                    is_blocked=value.is_blocked,
                    report_count=value.report_count,
                    read_count=value.read_count,
                    category=value.category,
                    last_user_action=value.last_user_action,
                    last_user_action_at=value.last_user_action_at,
                    last_admin_action=value.last_admin_action,
                    last_admin_action_at=value.last_admin_action_at,
                    created_at=value.created_at,
                    updated_at=value.updated_at,
                    user=value.user,
                )
            except ValidationError as e:
                print(e)
                return failure_response(
                    UseCaseFailureOutput(
                        type=FailureType.SYSTEM_ERROR,
                        message="response schema validation error",
                    )
                )
            result = {
                "data": {"post": schema.dict()},
                "meta": {"cursor": output.meta},
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)
