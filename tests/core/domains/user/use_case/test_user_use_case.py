import uuid

from app.persistence.model.post_model import PostModel
from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel
from core.domains.region.entity.region_entity import RegionEntity
from core.domains.user.dto.user_dto import GetUserDto
from core.domains.user.entity.user_profile_entity import UserProfileEntity
from core.domains.user.use_case.v1.user_use_case import GetUserUseCase


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
    assert isinstance(user_entity.user_profile, UserProfileEntity)
