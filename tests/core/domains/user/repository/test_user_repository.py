import uuid

from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel
from core.domains.user.repository.user_repository import UserRepository


def test_create_user_when_not_use_factory_boy(session):
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

    result = session.query(UserModel).first()

    assert result.nickname == user.nickname


def test_get_user(session):
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

    user_entity = UserRepository().get_user(user_id=user.id)

    assert user_entity == user.to_entity()
