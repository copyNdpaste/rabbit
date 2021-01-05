import uuid

from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel
from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostContentDto
from core.domains.board.use_case.v1.post_use_case import (
    CreatePostUseCase,
    UpdatePostContentUseCase,
)


def test_when_create_post_then_success(
    session, create_user, create_region, create_profile, create_post
):
    region = create_region
    profile = create_profile

    user = create_user(profile_id=profile.id, region_id=region.id)
    session.add(user)
    session.commit()

    dto = CreatePostDto(
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

    post_entity = CreatePostUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title


def test_when_update_post_content_then_success(
    session, create_user, create_region, create_profile, create_post
):
    region = create_region
    profile = create_profile

    user = create_user(profile_id=profile.id, region_id=region.id)
    session.add(user)
    session.commit()

    post = create_post(user_id=user.id)

    dto = UpdatePostContentDto(
        id=post.id,
        title="떡볶이 같이 먹어요",
        region_group_id=1,
        type="article",
        is_comment_disabled=True,
        category=0,
    )

    post_entity = UpdatePostContentUseCase().execute(dto=dto).value

    assert post_entity.title == dto.title
    assert post_entity.is_comment_disabled == dto.is_comment_disabled
