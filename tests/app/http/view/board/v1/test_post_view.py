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
        id=user.post[0].id,
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
    assert data["post"]["body"] == dct["body"]
