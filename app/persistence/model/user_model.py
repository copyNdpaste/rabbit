from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    SmallInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from core.domains.user.entity.user_entity import UserEntity


class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    login_id = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    profile_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        ForeignKey("user_profiles.id"),
        nullable=False,
    )
    status = Column(String(10), nullable=False)
    provider = Column(String(20), nullable=False)
    region_id = Column(SmallInteger, ForeignKey("regions.id"), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    user_profile = relationship("UserProfileModel", backref="user")
    region = relationship("RegionModel", backref="user")

    # def to_entity(self) -> UserEntity:
    #     return UserEntity(id=self.id, nickname=self.nickname)
