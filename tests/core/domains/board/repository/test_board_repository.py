import uuid

from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel
from core.domains.board.dto.post_dto import CreatePostDto
from core.domains.board.repository.board_repository import BoardRepository


def test_create_post(session):
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
        region_id=region.id,
    )
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