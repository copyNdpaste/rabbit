from core.domains.board.dto.post_dto import (
    CreatePostDto,
    UpdatePostDto,
    DeletePostDto,
    GetPostListDto,
    GetPostDto,
)
from core.domains.board.use_case.v1.post_use_case import (
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
    GetPostListUseCase,
    GetPostUseCase,
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
        post_id=user.post[0].id,
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
        post_id=user.post[0].id,
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
        post.region_group = user.region.region_group


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
    assert post_list[0].region_group.name == user.region.region_group.name


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
