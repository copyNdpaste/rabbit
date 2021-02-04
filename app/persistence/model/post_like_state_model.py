from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    SmallInteger,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.post_model import PostModel
from app.persistence.model.user_model import UserModel
from core.domains.board.entity.like_entity import PostLikeStateEntity


class PostLikeStateModel(db.Model):
    __tablename__ = "post_like_states"

    id = Column(SmallInteger().with_variant(Integer, "sqlite"), primary_key=True)
    post_id = Column(BigInteger, ForeignKey(PostModel.id), nullable=False)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    state = Column(String(10))
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    post = relationship("PostModel", backref="post_like_state")
    user = relationship("UserModel", backref="post_like_state")

    def to_entity(self) -> PostLikeStateEntity:
        return PostLikeStateEntity(
            id=self.id,
            post_id=self.post_id,
            user_id=self.user_id,
            state=self.state,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
