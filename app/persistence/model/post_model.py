from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    SmallInteger,
)
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from core.domains.board.entity.post_entity import PostEntity


class PostModel(db.Model):
    __tablename__ = "posts"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        ForeignKey("users.id"),
        nullable=False,
    )
    title = Column(String(100), nullable=False)
    region_group_id = Column(SmallInteger, nullable=False)
    type = Column(String(20), nullable=False)
    is_comment_disabled = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    is_blocked = Column(Boolean, nullable=False, default=False)
    report_count = Column(Integer, default=0)
    read_count = Column(Integer, default=0)
    category = Column(Integer, nullable=False)
    last_user_action = Column(String(20), nullable=False, default="default")
    last_user_action_at = Column(DateTime, default=get_server_timestamp())
    last_admin_action = Column(String(20), nullable=False, default="default")
    last_admin_action_at = Column(DateTime, default=get_server_timestamp())
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    user = relationship("UserModel", backref="post")

    def to_entity(self) -> PostEntity:
        return PostEntity(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            region_group_id=self.region_group_id,
            type=self.type,
            is_comment_disabled=self.is_comment_disabled,
            is_deleted=self.is_deleted,
            is_blocked=self.is_blocked,
            report_count=self.report_count,
            read_count=self.read_count,
            category=self.category,
            last_user_action=self.last_user_action,
            last_user_action_at=self.last_user_action_at,
            last_admin_action=self.last_admin_action,
            last_admin_action_at=self.last_admin_action_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user=self.user.to_entity(),
        )