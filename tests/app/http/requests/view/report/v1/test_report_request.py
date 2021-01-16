from app.http.requests.view.report.v1.report_request import CreatePostReportRequest
from core.domains.report.dto.post_report_dto import CreatePostReportDto


def test_create_post_repost_request_success():
    result = CreatePostReportRequest(
        post_id=1,
        report_user_id=2,
        status="pending",
        context="",
        confirm_admin_id=None,
        is_system_report=False,
    ).validate_request_and_make_dto()

    assert isinstance(result, CreatePostReportDto)


def test_create_post_repost_request_fail():
    result = CreatePostReportRequest(
        post_id=None,
        report_user_id=2,
        status="pending",
        context="",
        confirm_admin_id=None,
        is_system_report=False,
    ).validate_request_and_make_dto()

    assert result == False
