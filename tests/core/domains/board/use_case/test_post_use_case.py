from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto
from core.domains.board.use_case.v1.post_use_case import (
    CreatePostUseCase,
    UpdatePostUseCase,
)


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
        title="떡볶이 같이 먹어요",
        body="new body",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        category=0,
    )

    post_entity = UpdatePostUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title
    assert post_entity.body == dto.body
    assert post_entity.is_comment_disabled == dto.is_comment_disabled
