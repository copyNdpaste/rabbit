import io
from unittest.mock import patch

import pytest
from werkzeug.datastructures import FileStorage
from core.domains.region.entity.region_entity import RegionEntity
from core.domains.user.dto.user_dto import GetUserDto, UpdateUserDto
from core.domains.user.enum.user_enum import UserStatusEnum
from core.domains.user.use_case.v1.user_use_case import (
    GetUserUseCase,
    UpdateUserUseCase,
)


def test_when_get_user_then_success(session, normal_user_factory):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    dto = GetUserDto(user_id=user.id)

    user_entity = GetUserUseCase().execute(dto=dto).value

    assert user_entity.id == user.id


def test_when_get_user_with_relations_then_success(
    session, normal_user_factory, post_factory
):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    post = post_factory(
        Article=True, region_group_id=user.region.region_group.id, user_id=user.id
    )
    session.add(post)
    session.commit()

    dto = GetUserDto(user_id=user.id)

    user_entity = GetUserUseCase().execute(dto=dto).value

    assert user_entity.id == user.id
    assert isinstance(user_entity.region, RegionEntity)
    assert isinstance(user_entity.user_profile, str)


@pytest.mark.skip(reason="fox에서 처리되므로 스킵")
@patch("app.extensions.utils.image_helper.S3Helper.upload", return_value=True)
def test_when_update_user_then_success(
    upload_mock, session, normal_user_factory, region_factory
):
    user = normal_user_factory(Region=True, UserProfile=True)
    session.add(user)
    session.commit()

    region = region_factory()
    session.add(region)
    session.commit()

    # 실제 업로드 확인하려면 아래 경로에 이미지 첨부하고 patch 데코레이터 제거한 뒤 실행.
    file = FileStorage(
        stream=io.BytesIO(b"aaa"),
        filename="C:/project/rabbit/app/extensions/utils/a.jpg",
        content_type="multipart/form-data",
    )

    dto = UpdateUserDto(
        user_id=user.id,
        nickname="changed",
        status=UserStatusEnum.DEFAULT.value,
        region_id=region.id,
        files=[file],
    )

    user = UpdateUserUseCase().execute(dto=dto).value

    assert user.region_id == region.id
    assert user.nickname == dto.nickname
    assert isinstance(user.user_profile, str)
