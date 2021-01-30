from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from app.http.requests.view.board.v1.post_request import (
    CreatePostRequest,
    UpdatePostRequest,
    DeletePostRequest,
    GetPostListRequest,
    GetPostRequest,
)
from app.http.responses import failure_response
from app.http.responses.presenters.post_presenter import (
    PostPresenter,
    PostListPresenter,
)
from app.http.view import auth_required, api
from app.http.view.authentication import current_user
from core.domains.board.use_case.v1.post_use_case import (
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
    GetPostListUseCase,
    GetPostUseCase,
)
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


@api.route("/board/v1/posts", methods=["GET"])
@jwt_required
@auth_required
@swag_from("get_post_list.yml", methods=["GET"])
def get_post_list_view():
    dto = GetPostListRequest(**request.get_json()).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return PostListPresenter().transform(GetPostListUseCase().execute(dto=dto))


@api.route("/board/v1/post/<int:post_id>", methods=["GET"])
@jwt_required
@auth_required
@swag_from("get_post.yml", methods=["GET"])
def get_post_view(post_id):
    dto = GetPostRequest(post_id=post_id).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return PostPresenter().transform(GetPostUseCase().execute(dto=dto))


@api.route("/board/v1/posts", methods=["PUT"])
@jwt_required
@auth_required
@swag_from("update_post.yml", methods=["PUT"])
def update_post_view():
    dto = UpdatePostRequest(**request.get_json()).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return PostPresenter().transform(UpdatePostUseCase().execute(dto=dto))


@api.route("/board/v1/posts/<int:post_id>", methods=["DELETE"])
@jwt_required
@auth_required
@swag_from("delete_post.yml", methods=["DELETE"])
def delete_post_view(post_id):
    dto = DeletePostRequest(
        post_id=post_id, user_id=current_user.id
    ).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return PostPresenter().transform(DeletePostUseCase().execute(dto=dto))
