from sqlalchemy import Column, BigInteger, Integer, String, DateTime

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from core.domains.user.entity.user_profile_entity import UserProfileEntity


class UserProfileModel(db.Model):
    __tablename__ = "user_profiles"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    uuid = Column(String(length=50), nullable=False)
    file_name = Column(String(length=50), nullable=False)
    path = Column(String(length=100), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    def to_entity(self) -> UserProfileEntity:
        return UserProfileEntity(
            id=self.id,
            uuid=self.uuid,
            file_name=self.file_name,
            path=self.path,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
