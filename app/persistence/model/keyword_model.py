from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.persistence.model.user_model import UserModel


class KeywordModel(db.Model):
    __tablename__ = "keywords"

    user_id = Column(BigInteger().with_variant(Integer, "sqlite"), ForeignKey(UserModel.id), nullable=False)
    name_1 = Column(String(20), nullable=True)
    name_2 = Column(String(20), nullable=True)
    name_3 = Column(String(20), nullable=True)
    name_4 = Column(String(20), nullable=True)
    name_5 = Column(String(20), nullable=True)
    name_6 = Column(String(20), nullable=True)
    name_7 = Column(String(20), nullable=True)
    name_8 = Column(String(20), nullable=True)
    name_9 = Column(String(20), nullable=True)
    name_10 = Column(String(20), nullable=True)
    name_11 = Column(String(20), nullable=True)
    name_12 = Column(String(20), nullable=True)
    name_13 = Column(String(20), nullable=True)
    name_14 = Column(String(20), nullable=True)
    name_15 = Column(String(20), nullable=True)
    name_16 = Column(String(20), nullable=True)
    name_17 = Column(String(20), nullable=True)
    name_18 = Column(String(20), nullable=True)
    name_19 = Column(String(20), nullable=True)
    name_20 = Column(String(20), nullable=True)

    user = relationship("UserModel", backref="keywords")
