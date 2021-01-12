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
from app.persistence.model.post_model import PostModel
from core.domains.board.entity.report_entity import ReportEntity


class ReportModel(db.Model):
    __tablename__ = "reports"

    id = Column(SmallInteger().with_variant(Integer, "sqlite"), primary_key=True)
    ref_id = Column(
        BigInteger, ForeignKey([PostModel.id, CommentModel.id], nullable=False)
    )
    type = Column(String(20), nullable=False)
    report_user_id = Column(BigInteger, nullable=True)
    status = Column(String(20))
    context = Column(String(50))
    confirm_admin_id = Column(Integer)
    is_system_report = Column(Boolean)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    post = relationship("PostModel", backref="post")
    comment = relationship("CommentModel", backref="comment")

    def to_entity(self) -> ReportEntity:
        return ReportEntity(
            id=self.id,
            ref_id=self.ref_id,
            type=self.type,
            report_user_id=self.report_user_id,
            status=self.status,
            context=self.context,
            confirm_admin_id=self.confirm_admin_id,
            is_system_report=self.is_system_report,
            created_at=self.created_at,
        )
