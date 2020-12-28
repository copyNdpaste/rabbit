from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp


class PostModel(db.Model):
    __tablename__ = "posts"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        ForeignKey("users.id"),
        nullable=False,
    )
    title = Column(String(100), nullable=False)
    region_group_id = Column(String(50), nullable=False)  # TODO : region_groups 관계 필요?
    type = Column(String(20), nullable=False)
    is_comment_disabled = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean, nullable=False)
    is_blocked = Column(Boolean, nullable=False)
    report_count = Column(Integer)
    read_count = Column(Integer)
    category = Column(Integer, nullable=False)
    last_user_action = Column(String(20), nullable=False)
    last_user_action_at = Column(DateTime, default=get_server_timestamp())
    last_admin_action = Column(String(20), nullable=False)
    last_admin_action_at = Column(DateTime, default=get_server_timestamp())
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    user = relationship("UserModel", backref="post")
