from core.domains.report.dto.post_report_dto import CreatePostReportDto
from core.domains.report.use_case.v1.report_use_case import CreatePostReportUseCase
from core.use_case_output import FailureType


def test_when_create_post_report_then_success(app, session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    report_user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add_all([user, report_user])
    session.commit()

    dto = CreatePostReportDto(
        post_id=user.post[0].id,
        report_user_id=report_user.id,
        status="pending",
        context="",
        confirm_admin_id=None,
        is_system_report=False,
    )

    post_report = CreatePostReportUseCase().execute(dto=dto).value

    assert post_report.post_id == user.post[0].id


def test_when_create_post_report_without_post_then_not_found(
    app, session, normal_user_factory
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    report_user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add_all([user, report_user])
    session.commit()

    dto = CreatePostReportDto(
        post_id=0,
        report_user_id=report_user.id,
        status="pending",
        context="",
        confirm_admin_id=None,
        is_system_report=False,
    )

    result = CreatePostReportUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.NOT_FOUND_ERROR
