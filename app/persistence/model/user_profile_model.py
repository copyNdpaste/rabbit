from sqlalchemy import Column, BigInteger, Integer, String, DateTime

from app import db
from app.extensions.utils.time_helper import get_server_timestamp


class UserProfileModel(db.Model):
    __tablename__ = "user_profiles"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    uuid = Column(String(length=50), nullable=False)
    file_name = Column(String(length=50), nullable=False)
    path = Column(String(length=100), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())
