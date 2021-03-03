from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    ForeignKey, DateTime, Boolean,
)
from sqlalchemy.orm import relationship, backref

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.user_model import UserModel


class NotificationModel(db.Model):
    __tablename__ = "notifications"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        ForeignKey(UserModel.id),
        nullable=False,
    )
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())
    is_available = Column(Boolean, nullable=False, default=True)
    use_bantime = Column(Boolean, nullable=False, default=False)
    use_keyword = Column(Boolean, nullable=False, default=True)
    use_chat = Column(Boolean, nullable=False, default=True)
    use_etc = Column(Boolean, nullable=False, default=True)
    ban_time_from = Column(String(4), nullable=False, default="2300")
    ban_time_to = Column(String(4), nullable=False, default="0900")

    user = relationship("UserModel", backref="notifications")
