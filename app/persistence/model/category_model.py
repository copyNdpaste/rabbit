from sqlalchemy import Column, SmallInteger, String, DateTime

from app import db
from app.extensions.utils.time_helper import get_server_timestamp


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())
