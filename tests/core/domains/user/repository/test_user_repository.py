import uuid

import pytest

from app.extensions.utils.enum.aws_enum import S3PathEnum
from core.domains.user.enum.user_enum import UserStatusEnum
from core.domains.user.repository.user_repository import UserRepository


def test_get_user(session, normal_user_factory, add_and_commit):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    user_entity = UserRepository().get_user(user_id=user.id)

    assert user_entity == user.to_entity()


@pytest.mark.skip(reason="fox에서 처리되므로 스킵")
def test_update_user(session, normal_user_factory, region_factory, add_and_commit):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    region = region_factory()
    add_and_commit([region])

    user_entity = UserRepository().update_user(
        user_id=user.id,
        nickname="changed nickname",
        status=UserStatusEnum.DEFAULT.value,
        region_id=region.id,
    )

    assert user_entity.nickname == "changed nickname"
    assert user_entity.status == UserStatusEnum.DEFAULT.value
    assert user_entity.login_id == user.login_id
    assert user_entity.region_id == region.id


def test_get_user_profile(session, normal_user_factory, add_and_commit):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    user_profile = UserRepository().get_user_profile(user.profile_id)

    assert user_profile.id == user.profile_id


@pytest.mark.skip(reason="fox에서 처리되므로 스킵")
def test_update_user_profile(session, normal_user_factory, add_and_commit):
    user = normal_user_factory(Region=True, UserProfile=True)
    add_and_commit([user])

    uuid_ = str(uuid.uuid4())
    user_profile = UserRepository().update_user_profile(
        user_profile_id=user.profile_id,
        uuid=uuid_,
        file_name="changed",
        path=S3PathEnum.PROFILE_IMGS.value,
        extension=".png",
    )

    assert user_profile.uuid == uuid_
    assert user_profile.extension == ".png"
