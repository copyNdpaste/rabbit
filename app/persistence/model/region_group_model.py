from sqlalchemy import Column, Integer, String, SmallInteger, DateTime

from app import db
from app.extensions.utils.time_helper import get_server_timestamp
from core.domains.region.entity.region_group_entity import RegionGroupEntity


class RegionGroupModel(db.Model):
    __tablename__ = "region_groups"

    id = Column(SmallInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(length=50), nullable=False)
    created_at = Column(DateTime, default=get_server_timestamp())
    updated_at = Column(DateTime, default=get_server_timestamp())

    def to_entity(self) -> RegionGroupEntity:
        return RegionGroupEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
