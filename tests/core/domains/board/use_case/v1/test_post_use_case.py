import io
import pytest

from app.persistence.model.notification_history_model import NotificationHistoryModel
from unittest.mock import patch
from werkzeug.datastructures import FileStorage
from core.domains.board.dto.post_dto import (
    CreatePostDto,
    UpdatePostDto,
    DeletePostDto,
    GetPostListDto,
    GetPostDto,
    GetSellingPostListDto,
    GetLikePostListDto,
)
from core.domains.board.dto.post_like_dto import LikePostDto
from core.domains.board.enum.attachment_enum import AttachmentEnum
from core.domains.board.enum.post_enum import (
    PostCategoryEnum,
    PostUnitEnum,
    PostStatusEnum,
    PostLikeCountEnum,
    PostLikeStateEnum,
    PostLimitEnum,
    PostTypeEnum,
)
from core.domains.board.use_case.v1.post_use_case import (
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
    GetPostListUseCase,
    GetPostUseCase,
    LikePostUseCase,
    GetSellingPostListUseCase,
    GetLikePostListUseCase,
)
from core.domains.notification.enum.notification_enum import StatusEnum
from core.use_case_output import FailureType
from tests.seeder.factory import PostFactory, KeywordFactory, NotificationFactory


@patch("app.extensions.utils.image_helper.S3Helper.upload", return_value=True)
def test_when_create_post_then_success(
    upload_mock, session, normal_user_factory, create_categories, add_and_commit
):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    categories = create_categories(PostCategoryEnum.get_dict())

    # 실제 업로드 확인하려면 아래 경로에 이미지 첨부하고 patch 데코레이터 제거한 뒤 실행.
    file = FileStorage(
        stream=io.BytesIO(b"aaa"),
        filename="C:/project/rabbit/app/extensions/utils/a.jpg",
        content_type="multipart/form-data",
    )

    dto = CreatePostDto(
        user_id=user.id,
        title="떡볶이 나눠 먹어요",
        body="",
        region_group_id=1,
        type=PostTypeEnum.ATTACHMENT.value,
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
        file_type=AttachmentEnum.PICTURE.value,
        files=[file],
    )

    post_entity = CreatePostUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title
    assert post_entity.post_like_count == PostLikeCountEnum.DEFAULT.value
    assert isinstance(post_entity.attachments, list)


@patch("app.extensions.utils.image_helper.S3Helper.upload", return_value=True)
def test_when_update_post_then_success(
    upload_mock,
    session,
    normal_user_factory,
    article_factory,
    attachment_factory,
    add_and_commit,
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    add_and_commit([user])

    attachment = attachment_factory(post_id=user.post[0].id)
    add_and_commit([attachment])

    article = article_factory(post_id=user.post[0].id)
    add_and_commit([article])

    # 실제 업로드 확인하려면 아래 경로에 이미지 첨부하고 patch 데코레이터 제거한 뒤 실행.
    file = FileStorage(
        stream=io.BytesIO(b"aaa"),
        filename="C:/project/rabbit/app/extensions/utils/a.jpg",
        content_type="multipart/form-data",
    )

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
        file_type=AttachmentEnum.PICTURE.value,
        files=[file],
    )

    post_entity = UpdatePostUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title
    assert post_entity.body == dto.body
    assert post_entity.is_comment_disabled == dto.is_comment_disabled
    assert isinstance(post_entity.attachments, list)


# TODO: category update


def test_when_not_owner_update_post_then_fail(
    session, normal_user_factory, article_factory, add_and_commit
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    add_and_commit([user])

    article = article_factory(post_id=user.post[0].id)
    add_and_commit([article])

    dto = UpdatePostDto(
        post_id=user.post[0].id,
        user_id=-1,
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

    result = UpdatePostUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.INVALID_REQUEST_ERROR


def test_when_delete_post_then_success(
    session, normal_user_factory, post_factory, add_and_commit
):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    post = post_factory(Article=True, user_id=user.id)
    add_and_commit([post])

    dto = DeletePostDto(post_id=user.post[0].id, user_id=user.id)

    post_entity = DeletePostUseCase().execute(dto=dto).value

    assert post_entity.id == dto.post_id
    assert post_entity.is_deleted == True


def test_when_not_owner_delete_post_then_fail(
    session, normal_user_factory, post_factory, add_and_commit
):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    post = post_factory(Article=True, user_id=user.id)
    add_and_commit([post])

    dto = DeletePostDto(post_id=user.post[0].id, user_id=-1)

    result = DeletePostUseCase().execute(dto=dto).value

    assert result["type"] == FailureType.INVALID_REQUEST_ERROR


def test_when_get_post_list_then_success(
    session, normal_user_factory, post_factory, create_categories, add_and_commit
):
    """
    post list 조회 시 region에 맞는 관련 table 목록 가져옴.
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

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
    add_and_commit([user2])
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

    add_and_commit([post1, post2, post3, post4])

    dto = GetPostListDto(
        region_group_id=user.region.region_group.id, category_ids=[categories[0].id],
    )
    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 2
    for post in post_list:
        post.region_group_name = user.region.region_group.name


def test_when_get_empty_post_list_then_empty_list(
    session, normal_user_factory, create_categories, add_and_commit
):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    categories = create_categories(PostCategoryEnum.get_dict())

    dto = GetPostListDto(
        region_group_id=user.region.region_group.id, category_ids=[categories[0].id]
    )
    result = GetPostListUseCase().execute(dto=dto).value

    assert result == []


def test_when_get_post_list_pagination_then_success(
    session, normal_user_factory, create_categories, add_and_commit
):
    """
    post list 조회 시 페이지네이션
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    categories = create_categories(PostCategoryEnum.get_dict())

    post_list = PostFactory.create_batch(
        size=11,
        Article=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    add_and_commit(post_list)

    dto = GetPostListDto(
        region_group_id=user.region.region_group.id,
        previous_post_id=len(post_list) % PostLimitEnum.LIMIT.value + 1,
        category_ids=[categories[0].id],
    )
    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 1
    assert post_list[0].region_group_name == user.region.region_group.name


def test_when_deleted_or_blocked_post_then_except(
    session, normal_user_factory, post_factory, create_categories, add_and_commit
):
    """
    post list 조회 시 삭제, 차단된 게시글 제외
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    categories = create_categories(PostCategoryEnum.get_dict())

    post = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    deleted_post = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
        is_deleted=True,
    )
    blocked_post = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
        is_blocked=True,
    )

    add_and_commit([post, deleted_post, blocked_post])

    dto = GetPostListDto(
        region_group_id=user.region.region_group.id, category_ids=[categories[0].id],
    )
    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 1


def test_when_get_post_then_success(
    session, normal_user_factory, post_factory, attachment_factory, add_and_commit
):
    """
    post 조회
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])
    attachments = attachment_factory.build_batch(size=1)

    post = post_factory(
        Article=True,
        Attachments=attachments,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )

    add_and_commit([post])

    dto = GetPostDto(post_id=post.id)

    post_entity = GetPostUseCase().execute(dto=dto).value

    assert post_entity.id == dto.post_id
    assert post_entity.read_count == 1
    assert isinstance(post_entity.attachments, list)


def test_when_get_not_exist_post_then_not_found(session, add_and_commit):
    """
    없는 post 조회
    """
    dto = GetPostDto(post_id=0)

    result = GetPostUseCase().execute(dto=dto)

    assert result.type == FailureType.NOT_FOUND_ERROR


def test_when_search_post_list_then_success(
    session, normal_user_factory, post_factory, create_categories, add_and_commit
):
    """
    post 검색. user1 post 2개, user2 post 2개, user3 post 1개, 다른 지역 user4 post 1개
    총 5개 post 응답
    """
    user_list = normal_user_factory.build_batch(size=4, Region=True, UserProfile=True)
    add_and_commit(user_list)

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

    add_and_commit([post1, post2, post3, post4, post5, post6])

    dto = GetPostListDto(
        region_group_id=region_group_id,
        title=post1.title[2:6],
        category_ids=[categories[0].id],
    )

    post_list = GetPostListUseCase().execute(dto=dto).value

    for post in post_list:
        assert post.region_group_id == region_group_id
        assert post1.title[2:6] in post.title
    assert len(post_list) == 5


def test_when_post_like_first_then_create_post_like_state(
    session, normal_user_factory, post_factory, add_and_commit
):
    # 최초 찜하기
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    post = post_factory(
        Article=True,
        PostLikeCount=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    add_and_commit([post])

    dto = LikePostDto(user_id=user.id, post_id=post.id)

    post_entity = LikePostUseCase().execute(dto=dto).value

    assert post_entity.id == post.id
    assert post_entity.user_id == user.id
    assert post_entity.post_like_state == PostLikeStateEnum.LIKE.value
    assert post_entity.post_like_count == PostLikeCountEnum.UP.value


def test_when_post_like_then_update_post_like_state(
    session, normal_user_factory, post_factory, add_and_commit
):
    # 찜하기, 찜취소
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    post = post_factory(
        Article=True,
        PostLikeCount=True,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    add_and_commit([post])

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
    session,
    normal_user_factory,
    post_factory,
    like_post,
    create_categories,
    add_and_commit,
):
    """
    post list 조회 시 찜 개수 포함, 찜 상태 제외
    user1 -> post1 찜
    user2 -> post1 찜
    user2 -> post2 찜
    """
    user1 = normal_user_factory(Region=True, UserProfile=True)
    user2 = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user1, user2])

    categories = create_categories(PostCategoryEnum.get_dict())

    post1 = post_factory(
        Article=True,
        PostLikeCount=True,
        Categories=categories,
        region_group_id=user1.region.region_group.id,
        user_id=user1.id,
    )
    post2 = post_factory(
        Article=True,
        PostLikeCount=True,
        Categories=categories,
        region_group_id=user1.region.region_group.id,
        user_id=user1.id,
    )
    add_and_commit([post1, post2])

    # 찜하기
    like_post(user_id=user1.id, post_id=post1.id)
    like_post(user_id=user2.id, post_id=post1.id)
    like_post(user_id=user2.id, post_id=post2.id)

    dto = GetPostListDto(
        region_group_id=user1.region.region_group.id, category_ids=[categories[0].id],
    )
    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 2
    assert post_list[0].post_like_count == 1
    assert post_list[1].post_like_count == 2


@pytest.mark.parametrize(
    "post_status, input_status, result_count",
    [
        (PostStatusEnum.SELLING.value, PostStatusEnum.ALL.value, 2),
        (PostStatusEnum.COMPLETED.value, PostStatusEnum.EXCLUDE_COMPLETED.value, 1),
    ],
)
def test_when_get_post_list_by_status(
    post_status,
    input_status,
    result_count,
    session,
    normal_user_factory,
    post_factory,
    create_categories,
    add_and_commit,
):
    """
    post list 조회 시 판매중, 거래완료 상태에 따라 응답
    """
    user = normal_user_factory.build(Region=True, UserProfile=True)
    add_and_commit([user])

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

    add_and_commit([post1, post2])

    dto = GetPostListDto(
        region_group_id=region_group_id,
        category_ids=[categories[0].id],
        status=input_status,
    )

    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == result_count


def test_when_get_post_list_order_by_desc_then_success(
    session, normal_user_factory, create_categories, post_factory, add_and_commit
):
    """
    판매중, 거래완료 최신순으로 조회
    """
    user = normal_user_factory.build(Region=True, UserProfile=True)
    add_and_commit([user])

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
    add_and_commit([post1, post2, post3])

    dto = GetPostListDto(
        region_group_id=user.region.region_group_id,
        category_ids=[categories[0].id],
        status=PostStatusEnum.ALL.value,
    )

    post_list = GetPostListUseCase().execute(dto=dto).value

    assert len(post_list) == 3
    assert post_list[0].id == 3
    assert post_list[1].id == 2
    assert post_list[2].id == 1


@pytest.mark.parametrize("post_count_result, input_user_id", [(2, 1), (0, 2)])
def test_get_selling_post_list(
    post_count_result,
    input_user_id,
    session,
    normal_user_factory,
    create_categories,
    post_factory,
    add_and_commit,
):
    """
    판매 목록 조회
    """
    user_list = normal_user_factory.build_batch(size=2, Region=True, UserProfile=True)
    add_and_commit(user_list)

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

    add_and_commit([post1, post2])

    dto = GetSellingPostListDto(user_id=input_user_id)

    selling_post_list = GetSellingPostListUseCase().execute(dto=dto).value

    assert len(selling_post_list) == post_count_result


def test_get_like_post_list(
    session,
    normal_user_factory,
    create_categories,
    post_factory,
    post_like_state_factory,
    add_and_commit,
):
    """
    내가 찜한 게시글, 찜 안한 게시글 생성 후 찜한 게시글만 응답  확인
    """
    user_list = normal_user_factory.build_batch(size=2, Region=True, UserProfile=True)
    add_and_commit(user_list)

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
    add_and_commit([liked_post])

    post_like_state = post_like_state_factory(post_id=liked_post.id, user_id=user2.id)

    add_and_commit([post, post_like_state])

    dto = GetLikePostListDto(user_id=user2.id)

    like_post_list = GetLikePostListUseCase().execute(dto=dto).value

    assert len(like_post_list) == 1


def test_when_create_post_then_set_redis_notification(
    session, normal_user_factory, create_categories, add_and_commit
):
    user = normal_user_factory(
        Region=True, UserProfile=True, UserNotificationToken=True
    )
    add_and_commit([user])

    keyword = KeywordFactory.build()
    notification = NotificationFactory.build()
    add_and_commit([keyword, notification])

    categories = create_categories(PostCategoryEnum.get_dict())

    user2 = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user2])

    dto = CreatePostDto(
        user_id=user2.id,
        title="양파 나눠 먹어요",
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

    CreatePostUseCase().execute(dto=dto)

    notification_history = (
        session.query(NotificationHistoryModel)
        .filter(NotificationHistoryModel.id == 1)
        .first()
    )

    assert user.id == notification_history.user_id
    assert notification_history.status == StatusEnum.PENDING.value
