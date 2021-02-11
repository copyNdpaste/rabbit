import pytest
from flask import url_for
from flask_jwt_extended import create_access_token

from core.domains.board.enum.post_enum import (
    PostUnitEnum,
    PostStatusEnum,
    PostLikeStateEnum,
    PostLikeCountEnum,
    PostCategoryEnum,
)


def test_when_create_post_then_success(
    client,
    session,
    test_request_context,
    jwt_manager,
    make_header,
    normal_user_factory,
    create_categories,
):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_list())

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
        user_id=user.id,
        title="떡볶이 나눠 먹어요",
        body="안녕하세요",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        is_deleted=False,
        is_blocked=False,
        report_count=0,
        read_count=0,
        amount=10,
        unit=PostUnitEnum.UNIT.value,
        price_per_unit=10000,
        status=PostStatusEnum.SELLING.value,
        category_ids=[categories[0].id],
    )

    with test_request_context:
        response = client.post(
            url_for("api/rabbit.create_post_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post"]["user_id"] == user.id
    assert data["post"]["body"] == dct["body"]


def test_when_update_post_then_success(
    client,
    session,
    test_request_context,
    jwt_manager,
    make_header,
    normal_user_factory,
    article_factory,
    create_categories,
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    article = article_factory(post_id=user.post[0].id)
    session.add(article)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_list())

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
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
        category_ids=[categories[0].id],
    )

    with test_request_context:
        response = client.put(
            url_for("api/rabbit.update_post_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post"]["user_id"] == user.id


def test_when_delete_post_then_success(
    client,
    session,
    test_request_context,
    jwt_manager,
    make_header,
    normal_user_factory,
    article_factory,
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    article = article_factory(post_id=user.post[0].id)
    session.add(article)
    session.commit()

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)

    post_id = user.post[0].id

    with test_request_context:
        response = client.delete(
            url_for("api/rabbit.delete_post_view", post_id=post_id), headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post"]["id"] == user.post[0].id
    assert data["post"]["body"] == article.body


def test_when_get_post_list_then_success(
    client,
    session,
    test_request_context,
    make_header,
    normal_user_factory,
    post_factory,
    create_categories,
):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_list())

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

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
        region_group_id=user.region.region_group.id, category_ids=[categories[0].id],
    )

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_post_list_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    post_list = response.get_json()["data"]["post_list"]
    cursor = response.get_json()["meta"]["cursor"]
    assert post1.id == cursor["last_post_id"]
    assert post2.id == post_list[0]["id"]
    assert post1.id == post_list[1]["id"]


def test_when_get_post_then_success(
    client,
    session,
    test_request_context,
    make_header,
    normal_user_factory,
    post_factory,
):
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

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_post_view", post_id=post1.id), headers=headers
        )

    assert response.status_code == 200
    post = response.get_json()["data"]["post"]
    assert post1.id == post["id"]


def test_when_search_post_list_then_success(
    session,
    normal_user_factory,
    post_factory,
    make_header,
    test_request_context,
    client,
    create_categories,
):
    """
    post 검색
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    region_group_id = user.region.region_group_id

    categories = create_categories(PostCategoryEnum.get_list())

    post = post_factory(
        Article=True,
        Categories=categories,
        region_group_id=region_group_id,
        user_id=user.id,
    )

    session.add(post)
    session.commit()

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)

    dct = dict(
        region_group_id=region_group_id,
        title=post.title[2:6],
        category_ids=[categories[0].id],
    )

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_post_list_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    post_list = response.get_json()["data"]["post_list"]
    assert post_list[0]["id"] == post.id


def test_when_like_post_then_success(
    client,
    session,
    test_request_context,
    jwt_manager,
    make_header,
    normal_user_factory,
    post_factory,
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

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)

    post_id = user.post[0].id

    with test_request_context:
        response = client.post(
            url_for("api/rabbit.like_post_view", post_id=post_id), headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post"]["id"] == post_id
    assert data["post"]["user_id"] == user.id
    assert data["post"]["post_like_count"] == PostLikeCountEnum.UP.value
    assert data["post"]["post_like_state"] == PostLikeStateEnum.LIKE.value


def test_when_get_post_list_then_include_like_count_and_exclude_like_state(
    session,
    normal_user_factory,
    make_header,
    post_factory,
    like_post,
    test_request_context,
    client,
    create_categories,
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

    categories = create_categories(PostCategoryEnum.get_list())

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

    session.add_all([post1, post2])
    session.commit()

    # 찜하기
    like_post(user_id=user1.id, post_id=post1.id)
    like_post(user_id=user2.id, post_id=post1.id)
    like_post(user_id=user2.id, post_id=post2.id)

    access_token = create_access_token(identity=user1.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
        region_group_id=user1.region.region_group.id, category_ids=[categories[0].id],
    )

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_post_list_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post_list"][0]["post_like_count"] == 1
    assert data["post_list"][1]["post_like_count"] == 2


@pytest.mark.parametrize(
    "input_status, result_count",
    [(PostStatusEnum.SELLING.value, 2), (PostStatusEnum.COMPLETED.value, 1)],
)
def test_when_get_post_list_by_status_then_success(
    input_status,
    result_count,
    session,
    normal_user_factory,
    make_header,
    post_factory,
    like_post,
    test_request_context,
    client,
    create_categories,
):
    """
    post list 조회 시 판매중, 거래완료 상태에 따라 응답
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_list())

    post1 = post_factory(
        Article=True,
        PostLikeCount=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
    )
    post2 = post_factory(
        Article=True,
        PostLikeCount=True,
        Categories=categories,
        region_group_id=user.region.region_group.id,
        user_id=user.id,
        status=input_status,
    )

    session.add_all([post1, post2])
    session.commit()

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
        region_group_id=user.region.region_group.id, category_ids=[categories[0].id],
    )

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_post_list_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data["post_list"]) == result_count
