from typing import Optional

from app.extensions.database import session
from app.persistence.model.region_group_model import RegionGroupModel
from core.domains.region.entity.region_group_entity import RegionGroupEntity


class RegionRepository:
    def get_region_group(self, id: int) -> Optional[RegionGroupEntity]:
        region_group = session.query(RegionGroupModel).filter_by(id=id).first()

        return region_group.to_entity() if region_group else None
