from datetime import datetime

from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.entity.article_entity import ArticleEntity
from core.domains.board.repository.board_repository import BoardRepository
from core.domains.user.entity.user_entity import UserEntity
from tests.seeder.factory import PostFactory


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


def test_update_post(session, normal_user_factory, post_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post = post_factory(Article=True, user_id=user.id)
    session.add(post)
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

    post_entity = BoardRepository().update_post(dto=dto)

    assert post_entity.title == dto.title
    assert post_entity.article.body == dto.body
    assert post_entity.is_comment_disabled == dto.is_comment_disabled


def test_delete_post(session, normal_user_factory, post_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post = post_factory(Article=True, user_id=user.id)
    session.add(post)
    session.commit()

    dto = DeletePostDto(id=user.post[0].id, user_id=user.id)

    post_entity = BoardRepository().delete_post(dto=dto)

    assert post_entity.id == dto.id
    assert post_entity.is_deleted == True


def test_is_post_exist(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    result = BoardRepository().is_post_exist(post_id=user.post[0].id)

    assert result == True

    result = BoardRepository().is_post_exist(post_id=0)

    assert result == False


def test_get_post_list(session, normal_user_factory, post_factory):
    """
    post list 조회 시 관련 table 목록 가져옴.
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post1 = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id
    )
    post2 = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id
    )

    user2 = normal_user_factory(Region=True, UserProfile=True)
    session.add(user2)
    session.commit()
    post3 = post_factory(
        Article=True, region_group_id=user2.region.region_group.id, user_id=user2.id
    )
    post4 = post_factory(
        Article=True, region_group_id=user2.region.region_group.id, user_id=user2.id
    )

    session.add_all([post1, post2, post3, post4])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=user.region.region_group.id
    )

    assert len(post_list) == 2
    for post in post_list:
        post.region_group = user.region.region_group


def test_get_empty_post_list(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post_list = BoardRepository().get_post_list(region_group_id=0)

    assert post_list == []


def test_get_post_list_pagination(session, normal_user_factory):
    """
    post list 조회 시 페이지네이션
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post_list = PostFactory.create_batch(
        size=11,
        Article=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    session.add_all(post_list)
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=user.region.region_group.id, previous_post_id=10
    )

    assert len(post_list) == 1
    assert post_list[0].region_group.name == user.region.region_group.name


def test_get_post_list_except_deleted_or_blocked(
    session, normal_user_factory, post_factory
):
    """
    post list 조회 시 삭제, 차단된 게시글 제외
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    deleted_post = post_factory(
        Article=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
        is_deleted=True,
    )
    blocked_post = post_factory(
        Article=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
        is_blocked=True,
    )

    session.add_all([deleted_post, blocked_post])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=user.region.region_group.id
    )

    assert len(post_list) == 0


def test_get_post(session, normal_user_factory, post_factory):
    """
    post 조회 시 관련 table 목록 가져옴.
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post1 = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id
    )
    post2 = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id
    )

    session.add_all([post1, post2])
    session.commit()

    post_entity = BoardRepository().get_post(id=user.post[0].id)

    assert post_entity.id == user.post[0].id
    assert post_entity.is_deleted == False
    assert post_entity.is_blocked == False
    assert post_entity.read_count == 0
    assert post_entity.is_comment_disabled == False
    assert post_entity.region_group.name == user.post[0].region_group.name
    assert isinstance(post_entity.created_at, datetime)
    assert isinstance(post_entity.user, UserEntity)
    assert isinstance(post_entity.article, ArticleEntity)


def test_get_empty_post(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post = BoardRepository().get_post(id=0)

    assert post == None


def test_get_post_except_deleted_or_blocked(session, normal_user_factory, post_factory):
    """
    post 조회 시 삭제, 차단 정보 포함
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    deleted_post = post_factory(
        Article=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
        is_deleted=True,
    )
    blocked_post = post_factory(
        Article=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
        is_blocked=True,
    )
    session.add_all([deleted_post, blocked_post])
    session.commit()

    post_entity = BoardRepository().get_post(id=deleted_post.id)
    assert post_entity.is_deleted == True

    post_entity = BoardRepository().get_post(id=blocked_post.id)
    assert post_entity.is_blocked == True


def test_add_read_count(session, normal_user_factory, post_factory):
    """
    post 조회 시 read_count + 1
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id
    )
    session.add(post)
    session.commit()

    result = BoardRepository().add_read_count(id=post.id)

    assert result == True
