import pytest
from datetime import date, timedelta, datetime
from faker import Faker

from app.persistence.model.post_model import PostModel
from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_profile_model import UserProfileModel
from tests.seeder.factory import (
    PostFactory,
    RegionFactory,
    UserProfileFactory,
    UserFactory,
    ArticleFactory,
    RegionGroupFactory,
    PostLikeStateFactory,
)
from tests.seeder.factory.data_service_factory import NormalUserFactory

MODEL_FACTORIES = [
    NormalUserFactory,
    UserFactory,
    PostFactory,
    UserProfileFactory,
    RegionFactory,
    RegionGroupFactory,
    ArticleFactory,
    PostLikeStateFactory,
]


faker = Faker()


@pytest.fixture
def create_users(session, normal_user_factory):
    users = normal_user_factory.build_batch(2)

    session.add_all(users)
    session.commit()


def make_random_today_date(between_days: int = 1, year_ago: int = 2):
    """
        주어진 날의 00:00:00 ~ 23:59:59 사이의 랜덤 시간을 만든다.
        기본적으로 조회시간 기준 2년전으로 만듬
    """
    return faker.date_time_between_dates(
        datetime_start=date.today() - timedelta(days=365 * year_ago + between_days),
        datetime_end=datetime.now() - timedelta(days=365 * year_ago + between_days),
    )


def make_random_between_date(start_date, end_date):
    """주어진 날짜 사이의 랜덤 date 만든다 """
    return faker.date_time_between_dates(
        datetime_start=start_date, datetime_end=end_date
    )


@pytest.fixture
def create_user(session, user_factory):
    def _create_user(profile_id: int, region_id: int) -> UserModel:
        user = user_factory.build(profile_id=profile_id, region_id=region_id)
        session.add(user)
        session.commit()

        return user

    return _create_user


@pytest.fixture
def create_region(session, region_factory) -> RegionModel:
    region = region_factory.build()
    session.add(region)
    session.commit()

    return region


@pytest.fixture
def create_profile(session, user_profile_factory) -> UserProfileModel:
    user_profile = user_profile_factory.build()
    session.add(user_profile)
    session.commit()

    return user_profile


@pytest.fixture
def create_post(session, post_factory):
    def _create_post(user_id: int) -> PostModel:
        post = post_factory.build(user_id=user_id)
        session.add(post)
        session.commit()

        return post

    return _create_post
