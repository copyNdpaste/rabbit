from sqlalchemy import Column, BigInteger, Integer, String

from app import db


class NotificationTypeModel(db.Model):
    __tablename__ = "notification_types"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    category = Column(String(5), nullable=False)
    type = Column(String(3), nullable=False)
