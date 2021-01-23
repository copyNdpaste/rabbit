from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from app.persistence.model.region_group_model import RegionGroupModel
from core.domains.region.entity.region_entity import RegionEntity


class RegionModel(db.Model):
    __tablename__ = "regions"

    id = Column(SmallInteger().with_variant(Integer, "sqlite"), primary_key=True)
    region_group_id = Column(
        SmallInteger,
        ForeignKey(RegionGroupModel.id, ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(length=50), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    region_group = relationship("RegionGroupModel", backref="region")

    def to_entity(self) -> RegionEntity:
        return RegionEntity(
            id=self.id,
            region_group_id=self.region_group_id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
