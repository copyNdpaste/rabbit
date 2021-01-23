from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    SmallInteger,
    BigInteger,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.comment_model import CommentModel
from core.domains.board.entity.report_entity import PostReportEntity


class CommentReportModel(db.Model):
    __tablename__ = "comment_reports"

    id = Column(SmallInteger().with_variant(Integer, "sqlite"), primary_key=True)
    comment_id = Column(
        BigInteger, ForeignKey(CommentModel.id, ondelete="CASCADE"), nullable=False
    )
    report_user_id = Column(BigInteger, nullable=True)
    status = Column(String(20))
    context = Column(String(100))
    confirm_admin_id = Column(Integer)
    is_system_report = Column(Boolean)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    comment = relationship("CommentModel", backref="comment_report")

    def to_entity(self) -> PostReportEntity:
        return PostReportEntity(
            id=self.id,
            post_id=self.post_id,
            report_user_id=self.report_user_id,
            status=self.status,
            context=self.context,
            confirm_admin_id=self.confirm_admin_id,
            is_system_report=self.is_system_report,
            created_at=self.created_at,
        )
