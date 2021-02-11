from sqlalchemy import Column, SmallInteger, String, DateTime, Integer
from app import db
from app.extensions.utils.time_helper import get_server_timestamp


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = Column(SmallInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(40), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())
