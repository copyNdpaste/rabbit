import pytest

from core.domains.board.dto.post_dto import (
    CreatePostDto,
    UpdatePostDto,
    DeletePostDto,
    GetPostListDto,
    GetPostDto,
)
from core.domains.board.dto.post_like_dto import LikePostDto
from core.domains.board.enum.post_enum import (
    PostCategoryEnum,
    PostUnitEnum,
    PostStatusEnum,
    PostLikeCountEnum,
    PostLikeStateEnum,
)
from core.domains.board.use_case.v1.post_use_case import (
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
    GetPostListUseCase,
    GetPostUseCase,
    LikePostUseCase,
)
from core.use_case_output import FailureType
from tests.seeder.factory import PostFactory


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
        amount=10,
        unit=PostUnitEnum.UNIT.value,
        price_per_unit=10000,
        status=PostStatusEnum.SELLING.value,
    )

    post_entity = CreatePostUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title
    assert post_entity.post_like_count == PostLikeCountEnum.DEFAULT.value


def test_when_update_post_then_success(session, normal_user_factory, article_factory):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    article = article_factory(post_id=user.post[0].id)
    session.add(article)
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
        amount=10,
        unit=PostUnitEnum.UNIT.value,
        price_per_unit=10000,
        status=PostStatusEnum.SELLING.value,
    )

    post_entity = UpdatePostUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title
    assert post_entity.body == dto.body
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
        post_id=user.post[0].id,
        user_id=-1,
        title="떡볶이 같이 먹어요",
        body="new body",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        category=0,
        amount=10,
        unit=PostUnitEnum.UNIT.value,
        price_per_unit=10000,
        status=PostStatusEnum.SELLING.value,
    )

    result = UpdatePostUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.INVALID_REQUEST_ERROR


def test_when_delete_post_then_success(session, normal_user_factory, post_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post = post_factory(Article=True, user_id=user.id)
    session.add(post)
    session.commit()

    dto = DeletePostDto(post_id=user.post[0].id, user_id=user.id)

    post_entity = DeletePostUseCase().execute(dto=dto).value

    assert post_entity.id == dto.post_id
    assert post_entity.is_deleted == True


def test_when_not_owner_delete_post_then_fail(
    session, normal_user_factory, post_factory
):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post = post_factory(Article=True, user_id=user.id)
    session.add(post)
    session.commit()

    dto = DeletePostDto(post_id=user.post[0].id, user_id=-1)

    result = DeletePostUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.INVALID_REQUEST_ERROR


def test_when_get_post_list_then_success(session, normal_user_factory, post_factory):
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

    dto = GetPostListDto(region_group_id=user.region.region_group.id)
    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 2
    for post in post_list:
        post.region_group_name = user.region.region_group.name


def test_when_get_empty_post_list_then_not_found(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    dto = GetPostListDto(region_group_id=user.region.region_group.id)
    result = GetPostListUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.NOT_FOUND_ERROR


def test_when_get_post_list_pagination_then_success(session, normal_user_factory):
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

    dto = GetPostListDto(
        region_group_id=user.region.region_group.id, previous_post_id=10
    )
    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 1
    assert post_list[0].region_group_name == user.region.region_group.name


def test_when_deleted_or_blocked_post_then_except(
    session, normal_user_factory, post_factory
):
    """
    post list 조회 시 삭제, 차단된 게시글 제외
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id
    )
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

    session.add_all([post, deleted_post, blocked_post])
    session.commit()

    dto = GetPostListDto(region_group_id=user.region.region_group.id)
    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 1


def test_when_get_post_then_success(session, normal_user_factory, post_factory):
    """
    post 조회
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id
    )

    session.add(post)
    session.commit()

    dto = GetPostDto(post_id=post.id)

    post_entity = GetPostUseCase().execute(dto=dto).value

    assert post_entity.id == dto.post_id
    assert post_entity.read_count == 1


def test_when_get_not_exist_post_then_not_found(session):
    """
    없는 post 조회
    """
    dto = GetPostDto(post_id=0)

    result = GetPostUseCase().execute(dto=dto)

    assert result.type == FailureType.NOT_FOUND_ERROR


def test_when_search_post_list_then_success(session, normal_user_factory, post_factory):
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

    dto = GetPostListDto(region_group_id=region_group_id, title=post1.title[2:6])

    post_list = GetPostListUseCase().execute(dto=dto).value

    for post in post_list:
        assert post.region_group_id == region_group_id
        assert post1.title[2:6] in post.title
    assert len(post_list) == 5


def test_when_search_post_list_with_category_then_success(
    session, normal_user_factory, post_factory
):
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
        category=PostCategoryEnum.DIVIDING_FOOD_INGREDIENT.value,
    )
    post2 = post_factory(
        Article=True,
        region_group_id=region_group_id,
        user_id=user_list[0].id,
        category=PostCategoryEnum.DIVIDING_NECESSITIES.value,
    )
    post3 = post_factory(
        Article=True,
        region_group_id=region_group_id,
        user_id=user_list[1].id,
        category=PostCategoryEnum.DIVIDING_FOOD_INGREDIENT.value,
    )

    session.add_all([post1, post2, post3])
    session.commit()

    dto = GetPostListDto(
        region_group_id=region_group_id,
        category=PostCategoryEnum.DIVIDING_FOOD_INGREDIENT.value,
    )

    post_list = GetPostListUseCase().execute(dto=dto).value

    for post in post_list:
        assert post.region_group_id == region_group_id
        assert post.category == PostCategoryEnum.DIVIDING_FOOD_INGREDIENT.value
    assert len(post_list) == 2


def test_when_post_like_first_then_create_post_like_state(
    session, normal_user_factory, post_factory
):
    # 최초 찜하기
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)

    session.commit()
    post = post_factory(
        Article=True,
        PostLikeCount=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    session.add(post)
    session.commit()

    dto = LikePostDto(user_id=user.id, post_id=post.id)

    post_entity = LikePostUseCase().execute(dto=dto).value

    assert post_entity.id == post.id
    assert post_entity.user_id == user.id
    assert post_entity.post_like_state == PostLikeStateEnum.LIKE.value
    assert post_entity.post_like_count == PostLikeCountEnum.UP.value


def test_when_post_like_then_update_post_like_state(
    session, normal_user_factory, post_factory
):
    # 찜하기, 찜취소
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True,
        PostLikeCount=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    session.add(post)
    session.commit()

    dto = LikePostDto(user_id=user.id, post_id=post.id)

    post_entity = LikePostUseCase().execute(dto=dto).value

    assert post_entity.id == post.id
    assert post_entity.user_id == user.id
    assert post_entity.post_like_state == PostLikeStateEnum.LIKE.value
    assert post_entity.post_like_count == PostLikeCountEnum.UP.value

    post_entity = LikePostUseCase().execute(dto=dto).value

    assert post_entity.id == post.id
    assert post_entity.user_id == user.id
    assert post_entity.post_like_state == PostLikeStateEnum.UNLIKE.value
    assert post_entity.post_like_count == PostLikeCountEnum.DEFAULT.value


def test_when_get_post_list_then_include_like_count_and_exclude_like_state(
    session, normal_user_factory, post_factory, like_post
):
    """
    post list 조회 시 찜 개수 포함, 찜 상태 제외
    user1 -> post1 찜
    user2 -> post1 찜
    user2 -> post2 찜
    """
    user1 = normal_user_factory(Region=True, UserProfile=True)
    user2 = normal_user_factory(Region=True, UserProfile=True)
    session.add_all([user1, user2])
    session.commit()

    post1 = post_factory(
        Article=True,
        PostLikeCount=True,
        region_group_id=user1.region.region_group.id,
        user_id=user1.id,
    )
    post2 = post_factory(
        Article=True,
        PostLikeCount=True,
        region_group_id=user1.region.region_group.id,
        user_id=user1.id,
    )

    session.add_all([post1, post2])
    session.commit()

    # 찜하기
    like_post(user_id=user1.id, post_id=post1.id)
    like_post(user_id=user2.id, post_id=post1.id)
    like_post(user_id=user2.id, post_id=post2.id)

    dto = GetPostListDto(region_group_id=user1.region.region_group.id)
    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 2
    assert post_list[0].post_like_count == 1
    assert post_list[1].post_like_count == 2


@pytest.mark.parametrize(
    "input_status, result_count",
    [(PostStatusEnum.SELLING.value, 2), (PostStatusEnum.COMPLETED.value, 1)],
)
def test_when_get_post_list_by_status_then_success(
    input_status, result_count, session, normal_user_factory, post_factory
):
    """
    post list 조회 시 판매중, 거래완료 상태에 따라 응답
    """
    user = normal_user_factory.build(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    region_group_id = user.region.region_group_id

    post1 = post_factory(
        Article=True, region_group_id=region_group_id, user_id=user.id,
    )
    post2 = post_factory(
        Article=True,
        region_group_id=region_group_id,
        user_id=user.id,
        status=input_status,
    )

    session.add_all([post1, post2])
    session.commit()

    dto = GetPostListDto(region_group_id=user.region.region_group_id)

    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == result_count
