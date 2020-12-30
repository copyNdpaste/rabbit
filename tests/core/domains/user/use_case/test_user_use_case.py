import uuid

from app.persistence.model.post_model import PostModel
from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel
from core.domains.region.entity.region_entity import RegionEntity
from core.domains.user.dto.user_dto import GetUserDto
from core.domains.user.entity.user_profile_entity import UserProfileEntity
from core.domains.user.use_case.v1.user_use_case import GetUserUseCase


def test_when_get_user_then_success(session):
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

    dto = GetUserDto(user_id=user.id)

    user_entity = GetUserUseCase().execute(dto=dto).value

    assert user_entity.id == user.id


def test_when_get_user_with_relations_then_success(session):
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

    post = PostModel(
        user_id=user.id,
        title="떡볶이 나눠 먹어요",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        is_deleted=False,
        is_blocked=False,
        report_count=0,
        read_count=0,
        category=0,
        last_user_action="default",
        last_admin_action="default",
    )
    session.add(post)
    session.commit()

    dto = GetUserDto(user_id=user.id)

    user_entity = GetUserUseCase().execute(dto=dto).value

    assert user_entity.id == user.id
    assert isinstance(user_entity.region, RegionEntity)
    assert isinstance(user_entity.user_profile, UserProfileEntity)
