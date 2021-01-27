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
from sqlalchemy.orm import relationship, backref

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.region_group_model import RegionGroupModel
from app.persistence.model.user_model import UserModel
from core.domains.board.entity.post_entity import PostEntity, PostListEntity


class PostModel(db.Model):
    __tablename__ = "posts"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        ForeignKey(UserModel.id, ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String(100), nullable=False)
    region_group_id = Column(
        SmallInteger,
        ForeignKey(RegionGroupModel.id, ondelete="CASCADE"),
        nullable=False,
    )
    type = Column(String(20), nullable=False)
    is_comment_disabled = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    is_blocked = Column(Boolean, nullable=False, default=False)
    report_count = Column(Integer, default=0)
    read_count = Column(Integer, default=0)
    category = Column(Integer, nullable=False)
    last_user_action = Column(String(20), nullable=False, default="default")
    last_user_action_at = Column(DateTime, nullable=True)
    last_admin_action = Column(String(20), nullable=False, default="default")
    last_admin_action_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    user = relationship("UserModel", backref="post")
    region_group = relationship(
        "RegionGroupModel", backref=backref("post", uselist=False)
    )

    def to_entity(self) -> PostEntity:
        return PostEntity(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            body=self.article.body if self.article else None,
            region_group_id=self.region_group_id,
            region_group_name=self.region_group.name if self.region_group else None,
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
            user=self.user.to_entity() if self.user else None,
        )

    def to_post_list_entity(self) -> PostListEntity:
        # 게시글 리스트 응답용 entity
        return PostListEntity(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            body=self.article.body if self.article else None,
            region_name=self.user.region.name if self.user.region else None,
            region_group_id=self.region_group_id,
            region_group_name=self.user.region.region_group.name
            if self.user.region.region_group
            else None,
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
            user=self.user.to_entity() if self.user else None,
            user_profile=self.user.user_profile.to_entity()
            if self.user.user_profile
            else None,
        )
