from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    SmallInteger,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.post_model import PostModel
from core.domains.board.entity.like_entity import PostLikeCountEntity


class PostLikeCountModel(db.Model):
    __tablename__ = "post_like_counts"

    id = Column(SmallInteger().with_variant(Integer, "sqlite"), primary_key=True)
    post_id = Column(BigInteger, ForeignKey(PostModel.id), nullable=False)
    count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    post = relationship("PostModel", backref=backref("post_like_count", uselist=False))

    def to_entity(self) -> PostLikeCountEntity:
        return PostLikeCountEntity(
            id=self.id,
            post_id=self.post_id,
            count=self.count,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
