from core.domains.region.repository.region_repository import RegionRepository


def test_get_region_group(session, region_factory):
    region = region_factory()
    session.add(region)
    session.commit()

    region_group_entity = RegionRepository().get_region_group(id=region.region_group.id)

    assert region_group_entity is not None
