from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.repository.board_repository import BoardRepository


def test_create_post(session, normal_user_factory):
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

    post_entity = BoardRepository().create_post(dto=dto)

    assert post_entity.title == dto.title


def test_update_post(session, normal_user_factory, article_factory):
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

    post_entity = BoardRepository().update_post(dto=dto)

    assert post_entity.title == dto.title
    assert post_entity.body == dto.body
    assert post_entity.is_comment_disabled == dto.is_comment_disabled


def test_delete_post(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    dto = DeletePostDto(id=user.post[0].id)

    post_entity = BoardRepository().delete_post(dto=dto)

    assert post_entity.id == dto.id
    assert post_entity.is_deleted == True
