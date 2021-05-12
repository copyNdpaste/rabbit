import pytest
from flask import url_for

from core.use_case_output import FailureType


def test_when_user_id_exists_then_check_auth_success(
    client,
    session,
    test_request_context,
    jwt_manager,
    make_header,
    normal_user_factory,
    add_and_commit,
    make_authorization,
):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    authorization = make_authorization(user_id=user.id)
    headers = make_header(authorization=authorization)

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.auth_for_testing_view"), headers=headers
        )

    assert response.status_code == 200
    assert response.json["data"]["result"]["type"] == "success"
    assert response.json["meta"]["cursor"] is None


@pytest.mark.skip(reason="jwt 문제로 스킵")
def test_when_user_id_not_exists_then_check_auth_failure(
    client, session, test_request_context, jwt_manager, make_header, make_authorization
):
    authorization = make_authorization()
    headers = make_header(authorization=authorization)

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.auth_for_testing_view"), headers=headers
        )

    assert response.status_code == 401
    assert response.json["type"] == FailureType.UNAUTHORIZED_ERROR
    assert response.json["message"] == ""
