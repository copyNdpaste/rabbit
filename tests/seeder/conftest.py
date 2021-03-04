import pytest
from datetime import date, timedelta, datetime
from faker import Faker
from core.domains.board.dto.post_like_dto import LikePostDto
from core.domains.board.use_case.v1.post_use_case import LikePostUseCase
from tests.seeder.factory import (
    PostFactory,
    RegionFactory,
    UserProfileFactory,
    UserFactory,
    ArticleFactory,
    RegionGroupFactory,
    PostLikeStateFactory,
    PostLikeCountFactory,
    CategoryFactory,
    PostCategoryFactory,
    AttachmentFactory,
    NotificationFactory,
    KeywordFactory,
    UserNotificationTokenFactory,
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
    PostLikeCountFactory,
    CategoryFactory,
    PostCategoryFactory,
    AttachmentFactory,
    NotificationFactory,
    KeywordFactory,
    UserNotificationTokenFactory,
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
def like_post(session):
    def _like_post(user_id: int, post_id: int):
        dto = LikePostDto(user_id=user_id, post_id=post_id)
        LikePostUseCase().execute(dto=dto)

    return _like_post


@pytest.fixture
def create_categories(session, category_factory):
    def _create_categories(category_dict: dict):
        categories = []
        for k, v in category_dict.items():
            c = category_factory(id=k, name=v)
            categories.append(c)
        session.add_all(categories)
        session.commit()

        return categories

    return _create_categories
