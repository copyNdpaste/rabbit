from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    SmallInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_profile_model import UserProfileModel
from core.domains.user.entity.user_entity import UserEntity


class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    login_id = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    profile_id = Column(BigInteger, ForeignKey(UserProfileModel.id), nullable=False,)
    status = Column(String(10), nullable=False)
    provider = Column(String(20), nullable=False)
    region_id = Column(SmallInteger, ForeignKey(RegionModel.id), nullable=False,)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    user_profile = relationship(
        "UserProfileModel", backref=backref("user", uselist=False)
    )
    region = relationship("RegionModel", backref=backref("user", uselist=False))

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            login_id=self.login_id,
            nickname=self.nickname,
            profile_id=self.profile_id,
            status=self.status,
            provider=self.provider,
            region_id=self.region_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_profile=self.user_profile.to_entity(),
            region=self.region.to_entity(),
        )
