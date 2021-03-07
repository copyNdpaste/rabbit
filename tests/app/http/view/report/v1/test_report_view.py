from flask import url_for


def test_when_create_post_report_then_success(
    client,
    session,
    test_request_context,
    jwt_manager,
    make_header,
    normal_user_factory,
    add_and_commit,
    make_authorization,
):
    user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    report_user = normal_user_factory(Region=True, UserProfile=True, Post=True)
    add_and_commit([user, report_user])

    authorization = make_authorization(user_id=user.id)
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
