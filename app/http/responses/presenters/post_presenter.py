from typing import Union
from pydantic import ValidationError
from app.http.responses import failure_response, success_response
from core.domains.board.schema.post_schema import (
    PostResponseSchema,
    PostListResponseSchema,
)
from core.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput, FailureType


class PostPresenter:
    def transform(self, output: Union[UseCaseSuccessOutput, UseCaseFailureOutput]):
        if isinstance(output, UseCaseSuccessOutput):
            value = output.value
            try:
                schema = PostResponseSchema(post=value)
            except ValidationError as e:
                print(e)
                return failure_response(
                    UseCaseFailureOutput(
                        type=FailureType.SYSTEM_ERROR,
                        message="response schema validation error",
                    )
                )
            result = {
                "data": schema.dict(),
                "meta": output.meta,
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)


class PostListPresenter:
    def transform(self, output: Union[UseCaseSuccessOutput, UseCaseFailureOutput]):
        if isinstance(output, UseCaseSuccessOutput):
            value = output.value
            if value:
                try:
                    schema = PostListResponseSchema(post_list=value)
                except ValidationError as e:
                    print(e)
                    return failure_response(
                        UseCaseFailureOutput(
                            type=FailureType.SYSTEM_ERROR,
                            message="response schema validation error",
                        )
                    )
            result = {
                "data": schema.dict(exclude_unset={"post_like_state"})
                if value
                else {"post_list": []},
                "meta": output.meta,
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)
