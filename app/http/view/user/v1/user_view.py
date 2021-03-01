from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from app.http.requests.view.user.v1.user_request import (
    GetUserRequest,
    UpdateUserRequest,
)
from app.http.responses import failure_response
from app.http.responses.presenters.user_presenter import UserPresenter
from app.http.view import auth_required, api
from core.domains.user.use_case.v1.user_use_case import (
    GetUserUseCase,
    UpdateUserUseCase,
)
from core.use_case_output import FailureType, UseCaseFailureOutput


@api.route("/user/v1/users/<int:user_id>", methods=["GET"])
@jwt_required
@auth_required
@swag_from("get_user.yml", methods=["GET"])
def get_user_view(user_id):
    dto = GetUserRequest(user_id=user_id).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return UserPresenter().transform(GetUserUseCase().execute(dto=dto))


# fox에서 user 관련 처리하기 때문에 api 주석처리함
# @api.route("/user/v1/users/<int:user_id>", methods=["PUT"])
# @jwt_required
# @auth_required
# @swag_from("update_user.yml", methods=["PUT"])
# def update_user_view(user_id):
#     dto = UpdateUserRequest(
#         user_id=user_id, **request.form.to_dict(), files=request.files.getlist("files")
#     ).validate_request_and_make_dto()
#     if not dto:
#         return failure_response(
#             UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
#         )
#
#     return UserPresenter().transform(UpdateUserUseCase().execute(dto=dto))
