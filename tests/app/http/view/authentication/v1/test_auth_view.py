import uuid

from flask import url_for
from flask_jwt_extended import create_access_token

from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel
from core.use_case_output import FailureType


def test_when_user_id_exists_then_check_auth_success(
    client, session, test_request_context, jwt_manager, make_header
):
    user_profile = UserProfileModel(
        uuid=str(uuid.uuid4()), file_name="file", path="uploads/"
    )
    session.add(user_profile)
    session.commit()

    region = RegionModel(name="청담동")
    session.add(region)
    session.commit()

    user = UserModel(
        login_id="hello",
        nickname="Noah",
        password="1234",
        profile_id=user_profile.id,
        status="default",
        provider="",
        region_id=region.id,
    )
    session.add(user)
    session.commit()

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.auth_for_testing_view"), headers=headers
        )

    assert response.status_code == 200
    assert response.json["data"]["result"]["type"] == "success"
    assert response.json["meta"]["cursor"] is None


def test_when_user_id_not_exists_then_check_auth_failure(
    client, session, test_request_context, jwt_manager, make_header
):
    access_token = create_access_token(identity=None)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.auth_for_testing_view"), headers=headers
        )

    assert response.status_code == 401
    assert response.json["type"] == FailureType.UNAUTHORIZED_ERROR
    assert response.json["message"] == ""
