from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.notification_type_model import NotificationTypeModel
from app.persistence.model.user_model import UserModel
from sqlalchemy.dialects.postgresql import JSONB


class NotificationHistoryModel(db.Model):
    __tablename__ = "notification_histories"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(BigInteger().with_variant(Integer, "sqlite"), ForeignKey(UserModel.id), nullable=False)
    notification_id = Column(BigInteger().with_variant(Integer, "sqlite"), ForeignKey(NotificationTypeModel.id),
                             nullable=False)
    status = Column(String(5), nullable=True)
    message = Column(JSONB().with_variant(JSON, "sqlite"), nullable=False, default={})
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    user = relationship("UserModel", backref="notification_history")
    notification_tpye = relationship("NotificationTypeModel", backref="notification_history")