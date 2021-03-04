import io
import json
import pytest
from unittest.mock import patch
from flask import url_for
from flask_jwt_extended import create_access_token
from werkzeug.datastructures import FileStorage
from app.persistence.model.attachment_model import AttachmentModel
from core.domains.board.enum.attachment_enum import AttachmentEnum
from core.domains.board.enum.post_enum import (
    PostUnitEnum,
    PostStatusEnum,
    PostLikeStateEnum,
    PostLikeCountEnum,
    PostCategoryEnum,
)


@patch("app.extensions.utils.image_helper.S3Helper.upload", return_value=True)
def test_when_create_post_then_success(
    s3_upload_mock,
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

    categories = create_categories(PostCategoryEnum.get_dict())

    # 실제 업로드 확인하려면 아래 경로에 이미지 첨부하고 patch 데코레이터 제거한 뒤 실행.
    file = FileStorage(
        stream=io.BytesIO(b"aaa"),
        filename="C:/project/rabbit/app/extensions/utils/a.jpg",
        content_type="multipart/form-data",
    )

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(
        authorization=authorization, content_type="multipart/form-data", accept="*/*"
    )
    dct = dict(
        user_id=user.id,
        title="떡볶이 나눠 먹어요",
        body="안녕하세요",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        amount=10,
        unit=PostUnitEnum.UNIT.value,
        price_per_unit=10000,
        status=PostStatusEnum.SELLING.value,
        category_ids=json.dumps([categories[0].id, categories[1].id]),
        file_type=AttachmentEnum.PICTURE.value,
        files=[file],
    )

    with test_request_context:
        response = client.post(
            url_for("api/rabbit.create_post_view"), data=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post"]["user_id"] == user.id
    assert data["post"]["body"] == dct["body"]
    assert isinstance(data["post"]["category_ids"], list)

    attachment = (
        session.query(AttachmentModel).filter_by(post_id=data["post"]["id"]).first()
    )
    assert attachment.extension == ".jpg"


@patch("app.extensions.utils.image_helper.S3Helper.upload", return_value=True)
def test_when_update_post_then_success(
    s3_upload_mock,
    client,
    session,
    test_request_context,
    jwt_manager,
    make_header,
    normal_user_factory,
    article_factory,
    create_categories,
    attachment_factory,
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add(user)
    session.commit()

    attachment = attachment_factory(post_id=user.post[0].id)
    session.add(attachment)
    session.commit()

    article = article_factory(post_id=user.post[0].id)
    session.add(article)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_dict())

    # 실제 업로드 확인하려면 아래 경로에 이미지 첨부하고 patch 데코레이터 제거한 뒤 실행.
    file = FileStorage(
        stream=io.BytesIO(b"aaa"),
        filename="C:/project/rabbit/app/extensions/utils/a.jpg",
        content_type="multipart/form-data",
    )

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(
        authorization=authorization, content_type="multipart/form-data", accept="*/*"
    )
    dct = dict(
        user_id=user.id,
        title="떡볶이 같이 먹어요",
        body="new body",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        category_ids=json.dumps([categories[0].id, categories[1].id]),
        amount=10,
        unit=PostUnitEnum.UNIT.value,
        price_per_unit=10000,
        status=PostStatusEnum.SELLING.value,
        file_type=AttachmentEnum.PICTURE.value,
        files=[file],
    )

    with test_request_context:
        response = client.put(
            url_for("api/rabbit.update_post_view", post_id=user.post[0].id),
            data=dct,
            headers=headers,
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post"]["user_id"] == user.id
    attachment = (
        session.query(AttachmentModel).filter_by(post_id=data["post"]["id"]).first()
    )
    assert attachment.extension == ".jpg"


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

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
        region_group_id=user.region.region_group.id,
        category_ids=[categories[0].id],
        status=PostStatusEnum.SELLING.value,
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

    categories = create_categories(PostCategoryEnum.get_dict())

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
        status=PostStatusEnum.SELLING.value,
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
        region_group_id=user1.region.region_group.id,
        category_ids=[categories[0].id],
        status=PostStatusEnum.SELLING.value,
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
    "post_status, input_status, result_count",
    [
        (PostStatusEnum.SELLING.value, PostStatusEnum.ALL.value, 2),
        (PostStatusEnum.COMPLETED.value, PostStatusEnum.EXCLUDE_COMPLETED.value, 1),
    ],
)
def test_when_get_post_list_by_status_then_success(
    post_status,
    input_status,
    result_count,
    session,
    normal_user_factory,
    make_header,
    like_post,
    test_request_context,
    client,
    create_categories,
    post_factory,
):
    """
    post list 조회 시 판매중, 거래완료 상태에 따라 응답
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    categories = create_categories(PostCategoryEnum.get_dict())

    region_group_id = user.region.region_group_id

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

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
        region_group_id=user.region.region_group.id,
        category_ids=[categories[0].id],
        status=input_status,
    )

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_post_list_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data["post_list"]) == result_count


def test_when_get_post_list_order_by_desc_then_success(
    session,
    normal_user_factory,
    create_categories,
    post_factory,
    make_header,
    test_request_context,
    client,
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

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
        region_group_id=user.region.region_group.id,
        category_ids=[categories[0].id],
        status=PostStatusEnum.ALL.value,
    )

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_post_list_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data["post_list"]) == 3
    assert data["post_list"][0]["id"] == 3
    assert data["post_list"][1]["id"] == 2
    assert data["post_list"][2]["id"] == 1


@pytest.mark.parametrize("post_count_result, input_user_id", [(2, 1), (0, 2)])
def test_get_selling_post_list(
    post_count_result,
    input_user_id,
    session,
    normal_user_factory,
    create_categories,
    post_factory,
    make_header,
    test_request_context,
    client,
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

    access_token = create_access_token(identity=input_user_id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(user_id=input_user_id)

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_selling_post_list_view"), json=dct, headers=headers,
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data["post_list"]) == post_count_result


def test_when_get_like_post_list_then_success(
    session,
    normal_user_factory,
    make_header,
    like_post,
    test_request_context,
    client,
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

    access_token = create_access_token(identity=user2.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(user_id=user2.id)

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_like_post_list_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data["post_list"]) == 1
