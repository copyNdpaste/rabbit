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
    post_id = Column(
        BigInteger, ForeignKey(PostModel.id, ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        BigInteger, ForeignKey(UserModel.id, ondelete="CASCADE"), nullable=False
    )
    parent_id = Column(
        BigInteger, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False
    )
    report_user_id = Column(BigInteger, nullable=True)
    status = Column(String(20))
    context = Column(String(50))
    confirm_admin_id = Column(Integer)
    is_system_report = Column(Boolean)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    post = relationship("PostModel", backref="comments")
    user = relationship("UserModel", backref="comments")
    parent = relationship(lambda: CommentModel, remote_side=id, backref="child")

    def to_entity(self):
        pass
