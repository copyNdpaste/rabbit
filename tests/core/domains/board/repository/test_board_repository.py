from datetime import datetime

from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.enum.post_enum import PostCategoryEnum
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
        post_id=user.post[0].id,
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
    assert post_entity.body == dto.body
    assert post_entity.is_comment_disabled == dto.is_comment_disabled


def test_delete_post(session, normal_user_factory, post_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post = post_factory(Article=True, user_id=user.id)
    session.add(post)
    session.commit()

    dto = DeletePostDto(post_id=user.post[0].id, user_id=user.id)

    post_entity = BoardRepository().delete_post(dto=dto)

    assert post_entity.id == dto.post_id
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
        post.region_group_name = user.region.region_group.name


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
    assert post_list[0].region_group_name == user.region.region_group.name


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

    post_entity = BoardRepository().get_post(post_id=user.post[0].id)

    assert post_entity.id == user.post[0].id
    assert post_entity.body == user.post[0].article.body
    assert post_entity.is_deleted == False
    assert post_entity.is_blocked == False
    assert post_entity.read_count == 0
    assert post_entity.is_comment_disabled == False
    assert post_entity.region_group_name == user.post[0].region_group.name
    assert isinstance(post_entity.created_at, datetime)
    assert isinstance(post_entity.user, UserEntity)


def test_get_empty_post(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post = BoardRepository().get_post(post_id=0)

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

    post_entity = BoardRepository().get_post(post_id=deleted_post.id)
    assert post_entity.is_deleted == True

    post_entity = BoardRepository().get_post(post_id=blocked_post.id)
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

    result = BoardRepository().add_read_count(post_id=post.id)

    assert result == True


def test_search_post_list(session, normal_user_factory, post_factory):
    """
    post 검색. user1 post 2개, user2 post 2개, user3 post 1개, 다른 지역 user4 post 1개
    총 5개 post 응답
    """
    user_list = normal_user_factory.build_batch(size=4, Region=True, UserProfile=True)
    session.add_all(user_list)
    session.commit()

    region_group_id = user_list[0].region.region_group_id

    post1 = post_factory(
        Article=True, region_group_id=region_group_id, user_id=user_list[0].id,
    )
    post2 = post_factory(
        Article=True, region_group_id=region_group_id, user_id=user_list[0].id,
    )
    post3 = post_factory(
        Article=True, region_group_id=region_group_id, user_id=user_list[1].id,
    )
    post4 = post_factory(
        Article=True, region_group_id=region_group_id, user_id=user_list[1].id,
    )
    post5 = post_factory(
        Article=True, region_group_id=region_group_id, user_id=user_list[2].id,
    )
    post6 = post_factory(
        Article=True,
        region_group_id=user_list[3].region.region_group_id,
        user_id=user_list[3].id,
    )

    session.add_all([post1, post2, post3, post4, post5, post6])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=region_group_id, title=post1.title[2:6]
    )

    for post in post_list:
        assert post.region_group_id == region_group_id
        assert post1.title[2:6] in post.title
    assert len(post_list) == 5


def test_search_post_list_with_category(session, normal_user_factory, post_factory):
    """
    category 조건으로 post 검색.
    """
    user_list = normal_user_factory.build_batch(size=2, Region=True, UserProfile=True)
    session.add_all(user_list)
    session.commit()

    region_group_id = user_list[0].region.region_group_id

    post1 = post_factory(
        Article=True,
        region_group_id=region_group_id,
        user_id=user_list[0].id,
        category=PostCategoryEnum.FOOD,
    )
    post2 = post_factory(
        Article=True,
        region_group_id=region_group_id,
        user_id=user_list[0].id,
        category=PostCategoryEnum.HOME_APPLIANCE,
    )
    post3 = post_factory(
        Article=True,
        region_group_id=region_group_id,
        user_id=user_list[1].id,
        category=PostCategoryEnum.FOOD,
    )

    session.add_all([post1, post2, post3])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=region_group_id, category=PostCategoryEnum.FOOD
    )

    for post in post_list:
        assert post.region_group_id == region_group_id
        assert post.category == PostCategoryEnum.FOOD
    assert len(post_list) == 2
