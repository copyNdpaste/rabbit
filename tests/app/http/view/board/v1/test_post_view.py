import uuid

from flask import url_for
from flask_jwt_extended import create_access_token

from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel


def test_when_create_post_then_success(
    client, session, test_request_context, jwt_manager, make_header
):
    region = RegionModel(name="청담동")
    session.add(region)
    session.commit()

    profile = UserProfileModel(uuid=str(uuid.uuid4()), file_name="pic", path="uploads/")
    session.add(profile)
    session.commit()

    user = UserModel(
        login_id="test",
        nickname="Tester",
        password="123",
        profile_id=profile.id,
        status="",
        provider="",
        region_id=1,
    )
    session.add(user)
    session.commit()

    access_token = create_access_token(identity=user.id)
    authorization = "Bearer " + access_token
    headers = make_header(authorization=authorization)
    data = dict(
        user_id=user.id,
        title="떡볶이 나눠 먹어요",
        region_group_id="서울",
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
            url_for("api/rabbit.create_post_view"), json=data, headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["post"]["user_id"] == user.id
