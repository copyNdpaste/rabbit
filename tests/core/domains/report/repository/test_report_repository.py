from core.domains.report.dto.post_report_dto import CreatePostReportDto
from core.domains.report.repository.report_repository import ReportRepository


def test_when_create_post_report_then_success(session, normal_user_factory):
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
    post_report = ReportRepository().create_post_report(dto=dto)

    assert post_report.post_id == user.post[0].id
