from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

from app import db
from app.persistence.model.user_model import UserModel


class UserNotificationTokenModel(db.Model):
    __tablename__ = "user_notification_tokens"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        ForeignKey(UserModel.id),
        nullable=False,
    )
    token = Column(String(50), nullable=True)

    user = relationship("UserModel", backref="user_notification_tokens")
