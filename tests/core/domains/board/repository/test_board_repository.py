import uuid
import pytest
from datetime import datetime
from app.extensions.utils.enum.aws_enum import S3PathEnum
from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.enum.attachment_enum import AttachmentEnum
from core.domains.board.enum.post_enum import (
    PostCategoryEnum,
    PostUnitEnum,
    PostStatusEnum,
    PostLikeStateEnum,
    PostLikeCountEnum,
    PostLimitEnum,
)
from core.domains.board.repository.board_repository import BoardRepository
from core.domains.user.entity.user_entity import UserEntity
from tests.seeder.factory import PostFactory


def test_create_post(session, normal_user_factory, create_categories):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_dict())

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
        last_user_action="default",
        last_admin_action="default",
        amount=10,
        unit=PostUnitEnum.UNIT.value,
        price_per_unit=10000,
        status=PostStatusEnum.SELLING.value,
        category_ids=[categories[0].id],
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
        amount=10,
        unit=PostUnitEnum.UNIT.value,
        price_per_unit=10000,
        status=PostStatusEnum.SELLING.value,
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


def test_get_post_list(session, normal_user_factory, post_factory, create_categories):
    """
    post list 조회 시 관련 table 목록 가져옴.
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_dict())

    post1 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    post2 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )

    user2 = normal_user_factory(Region=True, UserProfile=True)
    session.add(user2)
    session.commit()
    post3 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=user2.region.region_group.id,
        user_id=user2.id,
    )
    post4 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=user2.region.region_group.id,
        user_id=user2.id,
    )

    session.add_all([post1, post2, post3, post4])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=user.region.region_group.id, category_ids=[categories[0].id]
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


def test_get_post_list_pagination(session, normal_user_factory, create_categories):
    """
    post list 조회 시 페이지네이션
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_dict())

    post_list = PostFactory.create_batch(
        size=11,
        Article=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    session.add_all(post_list)
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=user.region.region_group.id,
        previous_post_id=len(post_list) % PostLimitEnum.LIMIT.value + 1,
        category_ids=[categories[0].id],
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
        Article=True,
        Attachments=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    post2 = post_factory(
        Article=True,
        Attachments=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
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
    assert isinstance(post_entity.attachments, list)


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


def test_search_post_list(
    session, normal_user_factory, post_factory, create_categories
):
    """
    post 검색. user1 post 2개, user2 post 2개, user3 post 1개, 다른 지역 user4 post 1개
    총 5개 post 응답
    """
    user_list = normal_user_factory.build_batch(size=4, Region=True, UserProfile=True)
    session.add_all(user_list)
    session.commit()

    region_group_id = user_list[0].region.region_group_id

    categories = create_categories(PostCategoryEnum.get_dict())

    post1 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=region_group_id,
        user_id=user_list[0].id,
    )
    post2 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=region_group_id,
        user_id=user_list[0].id,
    )
    post3 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=region_group_id,
        user_id=user_list[1].id,
    )
    post4 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=region_group_id,
        user_id=user_list[1].id,
    )
    post5 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=region_group_id,
        user_id=user_list[2].id,
    )
    post6 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=user_list[3].region.region_group_id,
        user_id=user_list[3].id,
    )

    session.add_all([post1, post2, post3, post4, post5, post6])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=region_group_id,
        title=post1.title[2:6],
        category_ids=[categories[0].id],
    )

    for post in post_list:
        assert post.region_group_id == region_group_id
        assert post1.title[2:6] in post.title
    assert len(post_list) == 5


def test_create_post_like_state(session, normal_user_factory, post_factory):
    # 최초 찜하기
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id,
    )
    session.add(post)
    session.commit()

    post_like_state = BoardRepository().create_post_like_state(
        user_id=user.id, post_id=post.id
    )

    assert post_like_state.post_id == post.id
    assert post_like_state.user_id == user.id
    assert post_like_state.state == PostLikeStateEnum.LIKE.value


def test_like_post(session, normal_user_factory, post_factory, post_like_state_factory):
    # 최초 아닌 찜하기
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id,
    )
    session.add(post)
    session.commit()
    post_like_state = post_like_state_factory(user_id=user.id, post_id=post.id)
    session.add(post_like_state)
    session.commit()

    post_like_state = BoardRepository().update_post_like_state(
        user_id=user.id, post_id=post.id, state=PostLikeStateEnum.LIKE.value
    )

    assert post_like_state.post_id == post.id
    assert post_like_state.user_id == user.id
    assert post_like_state.state == PostLikeStateEnum.LIKE.value


def test_unlike_post_like(
    session, normal_user_factory, post_factory, post_like_state_factory
):
    # 찜취소
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id,
    )
    session.add(post)
    session.commit()
    post_like_state = post_like_state_factory(user_id=user.id, post_id=post.id)
    session.add(post_like_state)
    session.commit()

    post_like_state = BoardRepository().update_post_like_state(
        user_id=user.id, post_id=post.id, state=PostLikeStateEnum.UNLIKE.value
    )

    assert post_like_state.post_id == post.id
    assert post_like_state.user_id == user.id
    assert post_like_state.state == PostLikeStateEnum.UNLIKE.value


def test_when_like_post_then_up_post_like_count(
    session, normal_user_factory, post_factory
):
    # 찜하면 count + 1
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

    post_like_count = BoardRepository().get_post_like_count(post_id=post.id)
    assert post_like_count.count == PostLikeCountEnum.DEFAULT.value

    is_post_like_counted = BoardRepository().update_post_like_count(
        post_id=post.id, count=PostLikeCountEnum.UP.value
    )
    post_like_count = BoardRepository().get_post_like_count(post_id=post.id)
    assert post_like_count.count == PostLikeCountEnum.UP.value
    assert is_post_like_counted == True


def test_when_unlike_post_then_down_post_like_count(
    session, normal_user_factory, post_factory
):
    # 찜취소하면 count - 1
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True,
        PostLikeCount=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
        PostLikeCount__count=PostLikeCountEnum.UP.value,
    )
    session.add(post)
    session.commit()

    post_like_count = BoardRepository().get_post_like_count(post_id=post.id)
    assert post_like_count.count == PostLikeCountEnum.UP.value

    is_post_like_counted = BoardRepository().update_post_like_count(
        post_id=post.id, count=PostLikeCountEnum.DOWN.value
    )
    post_like_count = BoardRepository().get_post_like_count(post_id=post.id)
    assert post_like_count.count == PostLikeCountEnum.DEFAULT.value
    assert is_post_like_counted == True


def test_create_post_like_count(session, normal_user_factory, post_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()
    post = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id,
    )
    session.add(post)
    session.commit()

    post_like_count = BoardRepository().create_post_like_count(post_id=post.id)
    assert post_like_count.count == PostLikeCountEnum.DEFAULT.value


@pytest.mark.parametrize(
    "post_status, input_status, result_count",
    [
        (PostStatusEnum.SELLING.value, PostStatusEnum.ALL.value, 2),
        (PostStatusEnum.COMPLETED.value, PostStatusEnum.EXCLUDE_COMPLETED.value, 1),
    ],
)
def test_get_post_list_by_status(
    post_status,
    input_status,
    result_count,
    session,
    normal_user_factory,
    post_factory,
    create_categories,
):
    """
    post list 조회 시 판매중, 거래완료 상태에 따라 응답
    """
    user = normal_user_factory.build(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    region_group_id = user.region.region_group_id

    categories = create_categories(PostCategoryEnum.get_dict())

    post1 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=region_group_id,
        user_id=user.id,
    )
    post2 = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=region_group_id,
        user_id=user.id,
        status=post_status,
    )

    session.add_all([post1, post2])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=region_group_id, status=input_status
    )

    assert len(post_list) == result_count


@pytest.mark.parametrize(
    "input_category_ids, result_count",
    [
        ([PostCategoryEnum.DIVIDING_FOOD_INGREDIENT.value], 1),
        ([PostCategoryEnum.USED_TRADING.value], 2),
        ([PostCategoryEnum.LOST_MISSING.value], 0),
    ],
)
def test_get_post_list_by_category(
    input_category_ids,
    result_count,
    session,
    normal_user_factory,
    post_factory,
    create_categories,
):
    """
    post category에 해당되는 post 응답
    """
    user = normal_user_factory.build(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_dict())

    region_group_id = user.region.region_group_id

    post1 = post_factory(
        Article=True,
        Categories=[categories[0], categories[1], categories[3]],
        region_group_id=region_group_id,
        user_id=user.id,
    )
    post2 = post_factory(
        Article=True,
        Categories=[categories[3]],
        region_group_id=region_group_id,
        user_id=user.id,
    )

    session.add_all([post1, post2])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=region_group_id, category_ids=input_category_ids
    )

    assert len(post_list) == result_count


def test_get_post_list_order_by_desc(
    session, normal_user_factory, create_categories, post_factory
):
    """
    판매중, 거래완료 최신순으로 조회
    """
    user = normal_user_factory.build(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_dict())

    region_group_id = user.region.region_group_id

    post1 = post_factory(
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=user.id,
        status=PostStatusEnum.SELLING.value,
    )
    post2 = post_factory(
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=user.id,
        status=PostStatusEnum.COMPLETED.value,
    )
    post3 = post_factory(
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=user.id,
        status=PostStatusEnum.COMPLETED.value,
    )

    session.add_all([post1, post2, post3])
    session.commit()

    post_list = BoardRepository().get_post_list(
        region_group_id=region_group_id,
        category_ids=[categories[0].id],
        status=PostStatusEnum.ALL.value,
    )

    assert len(post_list) == 3
    assert post_list[0].id == 3
    assert post_list[1].id == 2
    assert post_list[2].id == 1


@pytest.mark.parametrize("post_count_result, input_user_id", [(2, 1), (0, 0)])
def test_get_selling_post_list(
    post_count_result,
    input_user_id,
    session,
    normal_user_factory,
    create_categories,
    post_factory,
):
    """
    판매 목록 조회
    """
    user_list = normal_user_factory.build_batch(size=2, Region=True, UserProfile=True)
    session.add_all(user_list)
    session.commit()

    post_owner = user_list[0]

    categories = create_categories(PostCategoryEnum.get_dict())

    region_group_id = post_owner.region.region_group_id

    post1 = post_factory(
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=post_owner.id,
        status=PostStatusEnum.SELLING.value,
    )
    post2 = post_factory(
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=post_owner.id,
        status=PostStatusEnum.COMPLETED.value,
    )

    session.add_all([post1, post2])
    session.commit()

    selling_post_list = BoardRepository().get_selling_post_list(user_id=input_user_id)

    assert len(selling_post_list) == post_count_result


def test_get_selling_post_list_pagination(
    session, normal_user_factory, create_categories, post_factory,
):
    """
    판매 목록 조회 페이지네이션
    """
    user = normal_user_factory.build(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_dict())

    region_group_id = user.region.region_group_id

    post_list = post_factory.build_batch(
        size=11,
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=user.id,
        status=PostStatusEnum.SELLING.value,
    )

    session.add_all(post_list)
    session.commit()

    selling_post_list = BoardRepository().get_selling_post_list(
        user_id=user.id, previous_post_id=len(post_list) % PostLimitEnum.LIMIT.value + 1
    )

    assert len(selling_post_list) == 1
    assert selling_post_list[0].id == post_list[0].id


def test_get_like_post_list_success(
    session,
    normal_user_factory,
    create_categories,
    post_factory,
    post_like_state_factory,
):
    """
    내가 찜한 게시글, 찜 안한 게시글 생성 후 찜한 게시글만 응답  확인
    """
    user_list = normal_user_factory.build_batch(size=2, Region=True, UserProfile=True)
    session.add_all(user_list)
    session.commit()

    user1 = user_list[0]
    user2 = user_list[1]

    categories = create_categories(PostCategoryEnum.get_dict())

    region_group_id = user1.region.region_group_id

    liked_post = post_factory(
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=user1.id,
        status=PostStatusEnum.SELLING.value,
    )
    post = post_factory(
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=user1.id,
        status=PostStatusEnum.SELLING.value,
    )
    session.add(liked_post)
    session.commit()

    post_like_state = post_like_state_factory(post_id=liked_post.id, user_id=user2.id)

    session.add_all([post, post_like_state])
    session.commit()

    like_post_list = BoardRepository().get_like_post_list(user_id=user2.id)

    assert len(like_post_list) == 1
    assert like_post_list[0].id == liked_post.id
    assert like_post_list[0].user_id == user1.id


def test_get_empty_like_post_list_success(
    session, normal_user_factory, create_categories, post_factory,
):
    """
    게시글 응답 빈 list 확인
    """
    user_list = normal_user_factory.build_batch(size=2, Region=True, UserProfile=True)
    session.add_all(user_list)
    session.commit()

    user1 = user_list[0]
    user2 = user_list[1]

    categories = create_categories(PostCategoryEnum.get_dict())

    region_group_id = user1.region.region_group_id

    post = post_factory(
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=user1.id,
        status=PostStatusEnum.SELLING.value,
    )
    session.add(post)
    session.commit()

    like_post_list = BoardRepository().get_like_post_list(user_id=user2.id)

    assert like_post_list == []


def test_get_like_post_list_pagination_success(
    session,
    normal_user_factory,
    create_categories,
    post_factory,
    post_like_state_factory,
):
    """
    내가 찜한 게시글 페이지네이션
    """
    user_list = normal_user_factory.build_batch(size=2, Region=True, UserProfile=True)
    session.add_all(user_list)
    session.commit()

    user1 = user_list[0]
    user2 = user_list[1]

    categories = create_categories(PostCategoryEnum.get_dict())

    region_group_id = user1.region.region_group_id

    liked_post_list = post_factory.build_batch(
        size=11,
        Article=True,
        Categories=[categories[0]],
        region_group_id=region_group_id,
        user_id=user1.id,
        status=PostStatusEnum.SELLING.value,
    )
    session.add_all(liked_post_list)
    session.commit()

    post_like_state_list = []
    for liked_post in liked_post_list:
        post_like_state_list.append(
            post_like_state_factory(post_id=liked_post.id, user_id=user2.id)
        )

    session.add_all(post_like_state_list)
    session.commit()

    like_post_list_result = BoardRepository().get_like_post_list(
        user_id=user2.id,
        previous_post_id=len(liked_post_list) % PostLimitEnum.LIMIT.value + 1,
    )

    assert len(like_post_list_result) == 1
    assert like_post_list_result[0].id == liked_post_list[0].id


def test_create_attachment(session, post_factory):
    post = post_factory()

    session.add(post)
    session.commit()

    attachment = BoardRepository().create_attachment(
        post_id=post.id,
        type=AttachmentEnum.PICTURE.value,
        file_name="hi",
        path=S3PathEnum.POST_IMGS.value,
        uuid=str(uuid.uuid4()),
        extension="jpg",
    )

    assert attachment.post_id == post.id
