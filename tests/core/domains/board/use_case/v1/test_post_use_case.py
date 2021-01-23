from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.use_case.v1.post_use_case import (
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
)
from core.use_case_output import FailureType


def test_when_create_post_then_success(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    dto = CreatePostDto(
        user_id=user.id,
        title="떡볶이 나눠 먹어요",
        body="",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        is_deleted=False,
        is_blocked=False,
        report_count=0,
        read_count=0,
        category=0,
        last_user_action="default",
        last_admin_action="default",
    )

    post_entity = CreatePostUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title


def test_when_update_post_then_success(session, normal_user_factory, article_factory):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    article = article_factory(post_id=user.post[0].id)
    session.add(article)
    session.commit()

    dto = UpdatePostDto(
        id=user.post[0].id,
        user_id=user.id,
        title="떡볶이 같이 먹어요",
        body="new body",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        category=0,
    )

    post_entity = UpdatePostUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title
    assert post_entity.article.body == dto.body
    assert post_entity.is_comment_disabled == dto.is_comment_disabled


def test_when_not_owner_update_post_then_fail(
    session, normal_user_factory, article_factory
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    article = article_factory(post_id=user.post[0].id)
    session.add(article)
    session.commit()

    dto = UpdatePostDto(
        id=user.post[0].id,
        user_id=-1,
        title="떡볶이 같이 먹어요",
        body="new body",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        category=0,
    )

    result = UpdatePostUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.INVALID_REQUEST_ERROR


def test_when_delete_post_then_success(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    dto = DeletePostDto(id=user.post[0].id, user_id=user.id)

    post_entity = DeletePostUseCase().execute(dto=dto).value

    assert post_entity.id == dto.id
    assert post_entity.is_deleted == True


def test_when_not_owner_delete_post_then_fail(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    dto = DeletePostDto(id=user.post[0].id, user_id=-1)

    result = DeletePostUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.INVALID_REQUEST_ERROR
