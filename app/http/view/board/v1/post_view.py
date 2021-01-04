from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from app.http.requests.view.board.v1.post_request import CreatePostRequest
from app.http.responses import failure_response
from app.http.responses.presenters.post_presenter import PostPresenter
from app.http.view import auth_required, api
from core.domains.board.use_case.v1.post_use_case import CreatePostUseCase
from core.use_case_output import FailureType, UseCaseFailureOutput


@api.route("/board/v1/posts", methods=["POST"])
@jwt_required
@auth_required
@swag_from("create_post.yml", methods=["POST"])
def create_post_view():
    dto = CreatePostRequest(**request.get_json()).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return PostPresenter().transform(CreatePostUseCase().execute(dto=dto))