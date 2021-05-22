import io
from unittest.mock import patch

import pytest
from flask import url_for
from werkzeug.datastructures import FileStorage

from core.domains.user.enum.user_enum import UserStatusEnum
from core.use_case_output import FailureType


def test_when_get_user_with_valid_user_id_then_success(
    client,
    session,
    test_request_context,
    jwt_manager,
    make_authorization,
    make_header,
    normal_user_factory,
    add_and_commit,
):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    authorization = make_authorization(user_id=user.id)
    headers = make_header(authorization=authorization)

    with test_request_context:
        response = client.get(
            url_for("api/rabbit.get_user_view", user_id=user.id), headers=headers,
        )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["user"]["id"] == user.id


def test_when_get_not_existing_user_then_failure(
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
            url_for("api/rabbit.get_user_view", user_id=9999), headers=headers,
        )

    assert response.status_code == 400
    assert response.get_json()["type"] == FailureType.NOT_FOUND_ERROR


@pytest.mark.skip(reason="fox에서 처리되므로 스킵")
@patch("app.extensions.utils.image_helper.S3Helper.upload", return_value=True)
def test_when_update_user_then_success(
    upload_mock,
    client,
    session,
    test_request_context,
    jwt_manager,
    make_header,
    normal_user_factory,
    region_factory,
    add_and_commit,
    make_authorization,
):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    authorization = make_authorization(user_id=user.id)
    headers = make_header(
        authorization=authorization, content_type="multipart/form-data", accept="*/*"
    )

    region = region_factory()
    session.add(region)
    session.commit()

    # 실제 업로드 확인하려면 아래 경로에 이미지 첨부하고 patch 데코레이터 제거한 뒤 실행.
    file = FileStorage(
        stream=io.BytesIO(b"aaa"),
        filename="C:/project/rabbit/app/extensions/utils/a.jpg",
        content_type="multipart/form-data",
    )

    dct = {
        "nickname": "changed",
        "status": UserStatusEnum.DEFAULT.value,
        "region_id": region.id,
        "files": [file],
    }

    with test_request_context:
        response = client.put(
            url_for("api/rabbit.update_user_view", user_id=user.id),
            data=dct,
            headers=headers,
        )

    assert response.status_code == 200
    user_entity = response.get_json()["data"]["user"]
    assert user_entity["id"] == user.id
    assert user_entity["nickname"] == dct["nickname"]
    assert isinstance(user_entity["user_profile"], str)
