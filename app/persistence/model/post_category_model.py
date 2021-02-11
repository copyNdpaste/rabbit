from sqlalchemy import Column, BigInteger, Integer, ForeignKey, SmallInteger

from app import db
from app.persistence.model.category_model import CategoryModel
from app.persistence.model.post_model import PostModel


class PostCategoryModel(db.Model):
    __tablename__ = "post_category"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    post_id = Column("post_id", BigInteger, ForeignKey(PostModel.id))
    category_id = Column("category_id", SmallInteger, ForeignKey(CategoryModel.id))
