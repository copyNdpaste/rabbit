from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    SmallInteger,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.post_model import PostModel
from core.domains.board.entity.article_entity import ArticleEntity


class ArticleModel(db.Model):
    __tablename__ = "articles"

    id = Column(SmallInteger().with_variant(Integer, "sqlite"), primary_key=True)
    post_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        ForeignKey(PostModel.id),
        nullable=False,
    )
    # TODO : 성능상 글자 수 변경될 수 있음.
    body = Column(String(length=2000), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    post = relationship("PostModel", backref=backref("article", uselist=False))

    def to_entity(self) -> ArticleEntity:
        return ArticleEntity(
            id=self.id,
            post_id=self.post_id,
            body=self.body,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
