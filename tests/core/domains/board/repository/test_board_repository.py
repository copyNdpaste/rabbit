from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostContentDto
from core.domains.board.repository.board_repository import BoardRepository


def test_create_post(session, create_user, create_region, create_profile):
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

    post_entity = BoardRepository().create_post(dto=dto)

    assert post_entity.title == dto.title


def test_update_post(session, create_user, create_region, create_profile, create_post):
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

    post_entity = BoardRepository().update_post(dto=dto)

    assert post_entity.title == dto.title
    assert post_entity.is_comment_disabled == dto.is_comment_disabled
