from typing import Optional
from app.extensions.database import session
from app.extensions.utils.log_helper import logger_
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel
from core.domains.user.entity.user_entity import UserEntity
from core.domains.user.entity.user_profile_entity import UserProfileEntity
from core.exceptions import UserNotFoundException

logger = logger_.getLogger(__name__)


class UserRepository:
    def get_user(self, user_id: int) -> Optional[UserEntity]:
        user = session.query(UserModel).filter_by(id=user_id).first()

        if not user:
            raise UserNotFoundException
        return user.to_entity()

    def update_user(
        self, user_id: int, nickname: str, status: str, region_id: int
    ) -> Optional[UserEntity]:
        try:
            session.query(UserModel).filter_by(id=user_id).update(
                {"nickname": nickname, "status": status, "region_id": region_id}
            )
            return self.get_user(user_id=user_id)
        except Exception as e:
            logger.error(
                f"[UserRepository][update_user] user_id : {user_id} error : {e}"
            )
            session.rollback()
            return None

    def get_user_profile(self, user_profile_id: int) -> Optional[UserProfileEntity]:
        user_profile = (
            session.query(UserProfileModel).filter_by(id=user_profile_id).first()
        )
        if user_profile:
            return user_profile.to_entity()
        return None

    def update_user_profile(
        self, user_profile_id: int, uuid: str, file_name: str, path: str, extension: str
    ) -> Optional[UserProfileEntity]:
        try:
            session.query(UserProfileModel).filter_by(id=user_profile_id).update(
                {
                    "uuid": uuid,
                    "file_name": file_name,
                    "path": path,
                    "extension": extension,
                }
            )
            return self.get_user_profile(user_profile_id=user_profile_id)
        except Exception as e:
            logger.error(
                f"[UserRepository][update_user] user_profile_id : {user_profile_id} error : {e}"
            )
            session.rollback()
            return None
