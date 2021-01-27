from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from app.http.requests.view.report.v1.report_request import CreatePostReportRequest
from app.http.responses import failure_response
from app.http.responses.presenters.report_presenter import PostReportPresenter
from app.http.view import auth_required, api
from core.domains.report.use_case.v1.report_use_case import CreatePostReportUseCase
from core.use_case_output import UseCaseFailureOutput, FailureType


@api.route("/report/v1/posts", methods=["POST"])
@jwt_required
@auth_required
# @swag_from("create_post_report.yml", methods=["POST"])
def create_post_report_view():
    dto = CreatePostReportRequest(**request.get_json()).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return PostReportPresenter().transform(CreatePostReportUseCase().execute(dto=dto))
