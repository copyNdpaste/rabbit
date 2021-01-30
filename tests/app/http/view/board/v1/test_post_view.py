from flask import url_for
from flask_jwt_extended import create_access_token


def test_when_create_post_then_success(
    client, session, test_request_context, jwt_manager, make_header, normal_user_factory
):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

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
        category=0,
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
    dct = dict(
        post_id=user.post[0].id,
        user_id=user.id,
        title="떡볶이 같이 먹어요",
        body="new body",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        category=0,
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

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(region_group_id=user.region.region_group.id)

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
):
    """
    post 검색
    """
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    region_group_id = user.region.region_group_id

    post = post_factory(Article=True, region_group_id=region_group_id, user_id=user.id,)

    session.add(post)
    session.commit()

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)

    dct = dict(region_group_id=region_group_id, title=post.title[2:6])

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_post_list_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    post_list = response.get_json()["data"]["post_list"]
    assert post_list[0]["id"] == post.id
