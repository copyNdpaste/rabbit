from typing import Optional

from app.extensions.utils.event_observer import send_message, get_event_object
from core.domains.board.entity.post_entity import PostEntity
from core.domains.board.enum import PostTopicEnum
from core.domains.report.dto.post_report_dto import CreatePostReportDto
from core.domains.report.use_case.v1.report_use_case import CreatePostReportUseCase
from core.use_case_output import FailureType


def test_when_create_post_report_then_success(
    app, session, normal_user_factory, add_and_commit
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    report_user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    add_and_commit([user, report_user])

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
    app, session, normal_user_factory, add_and_commit
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    report_user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    add_and_commit([user, report_user])

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


def test_when_post_report_already_exist_then_fail(
    app, session, normal_user_factory, add_and_commit
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    report_user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    add_and_commit([user, report_user])

    dto = CreatePostReportDto(
        post_id=user.post[0].id,
        report_user_id=report_user.id,
        status="pending",
        context="",
        confirm_admin_id=None,
        is_system_report=False,
    )

    CreatePostReportUseCase().execute(dto=dto)
    result = CreatePostReportUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.ALREADY_EXIST


def test_when_post_report_over_max_then_block_post(
    app, session, normal_user_factory, add_and_commit, post_report_factory
):
    user = normal_user_factory(
        Region=True, UserProfile=True, Post=True, Post__report_count=2
    )

    report_user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    add_and_commit([user, report_user])

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

    post = _get_post(post_id=user.post[0].id)

    assert post.report_count == 3
    assert post.is_blocked == True


def _get_post(post_id: int) -> Optional[PostEntity]:
    send_message(
        topic_name=PostTopicEnum.GET_POST.value, post_id=post_id, is_blocked=True
    )

    return get_event_object(topic_name=PostTopicEnum.GET_POST.value)
