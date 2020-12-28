from sqlalchemy import Column, Integer, String, DateTime

from app import db
from app.extensions.utils.time_helper import get_server_timestamp


class RegionModel(db.Model):
    __tablename__ = "regions"

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True,)
    name = Column(String(length=50), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())
