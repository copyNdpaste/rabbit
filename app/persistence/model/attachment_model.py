from sqlalchemy import Column, BigInteger, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.post_model import PostModel
import uuid

from core.domains.board.entity.attachment_entiry import AttachmentEntity


class AttachmentModel(db.Model):
    __tablename__ = "attachments"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    post_id = Column(BigInteger, ForeignKey(PostModel.id), nullable=False)
    type = Column(String(10), nullable=False)
    uuid = Column(String(50), default=uuid.uuid4(), nullable=False)
    file_name = Column(String(50), nullable=False)
    path = Column(String(50), nullable=False)
    extension = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=get_server_timestamp())
    updated_at = Column(DateTime(), default=get_server_timestamp())

    post = relationship("PostModel", backref="attachments")

    def to_entity(self) -> AttachmentEntity:
        return AttachmentEntity(
            id=self.id,
            post_id=self.post_id,
            type=self.type,
            uuid=self.uuid,
            file_name=self.file_name,
            path=self.path,
            extension=self.extension,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
