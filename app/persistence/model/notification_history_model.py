from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    ForeignKey,
    DateTime,
    JSON,
    SmallInteger,
)
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.user_model import UserModel
from sqlalchemy.dialects.postgresql import JSONB


class NotificationHistoryModel(db.Model):
    __tablename__ = "notification_histories"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        ForeignKey(UserModel.id),
        nullable=False,
    )
    status = Column(String(5), nullable=True)
    message = Column(JSONB().with_variant(JSON, "sqlite"), nullable=False, default={})
    category = Column(String(5), nullable=False)
    type = Column(String(3), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    user = relationship("UserModel", backref="notification_history")
