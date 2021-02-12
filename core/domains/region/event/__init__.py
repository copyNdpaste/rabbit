from flask import g
from pubsub import pub

from core.domains.region.enum import RegionTopicEnum
from core.domains.region.repository.region_repository import RegionRepository


def get_region_group(id: int):
    region_group = RegionRepository().get_region_group(id=id)

    setattr(g, RegionTopicEnum.GET_REGION_GROUP, region_group)


pub.subscribe(get_region_group, RegionTopicEnum.GET_REGION_GROUP)
