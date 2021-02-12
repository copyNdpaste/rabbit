from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    BigInteger,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.post_model import PostModel
from app.persistence.model.user_model import UserModel


class CommentModel(db.Model):
    __tablename__ = "comments"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    post_id = Column(BigInteger, ForeignKey(PostModel.id), nullable=False)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    parent_id = Column(BigInteger, ForeignKey("comments.id"), nullable=False)
    body = Column(String(500))
    is_deleted = Column(Boolean, nullable=False, default=False)
    is_blocked = Column(Boolean, nullable=False, default=False)
    report_count = Column(Integer, default=0)
    last_user_action = Column(String(20), nullable=False, default="default")
    last_user_action_at = Column(DateTime, nullable=True)
    last_admin_action = Column(String(20), nullable=False, default="default")
    last_admin_action_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    post = relationship("PostModel", backref="comments")
    user = relationship("UserModel", backref="comments")
    parent = relationship(lambda: CommentModel, remote_side=id, backref="child")

    def to_entity(self):
        pass
