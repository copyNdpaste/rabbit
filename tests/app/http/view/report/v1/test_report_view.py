from flask import url_for
from flask_jwt_extended import create_access_token


def test_when_create_post_report_then_success(
    client, session, test_request_context, jwt_manager, make_header, normal_user_factory
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    report_user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    session.add_all([user, report_user])
    session.commit()

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    dct = dict(
        post_id=user.post[0].id,
        report_user_id=report_user.id,
        status="pending",
        context="",
        confirm_admin_id=None,
        is_system_report=False,
    )

    with test_request_context:
        response = client.post(
            url_for("api/rabbit.create_post_report_view"), json=dct, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post_report"]["post_id"] == user.post[0].id
