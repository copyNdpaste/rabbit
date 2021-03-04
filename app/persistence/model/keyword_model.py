from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import db
from app.persistence.model.user_model import UserModel


class KeywordModel(db.Model):
    __tablename__ = "keywords"

    user_id = Column(BigInteger().with_variant(Integer, "sqlite"), ForeignKey(UserModel.id), nullable=False)
    name_1 = Column(String(20), nullable=True)
    name_2 = Column(String(20), nullable=True)
    name_3 = Column(String(20), nullable=True)

    user = relationship("UserModel", backref="keywords")

    __mapper_args__ = {"primary_key": [user_id]}
