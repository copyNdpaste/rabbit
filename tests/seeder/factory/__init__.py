import factory
from faker import Factory as FakerFactory
import uuid

from app.extensions.database import session
from app.persistence.model.article_model import ArticleModel
from app.persistence.model.post_model import PostModel
from app.persistence.model.region_group_model import RegionGroupModel
from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel

# factory에 사용해야 하는 Model을 가져온다
from app.persistence.model.user_profile_model import UserProfileModel

faker = FakerFactory.create(locale="ko_KR")


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Define user factory
    """

    class Meta:
        model = UserModel

    login_id = factory.Sequence(lambda n: "test_user_{}".format(n))
    nickname = factory.Sequence(lambda n: "test_user_{}".format(n))
    password = "1234"
    profile_id = 1
    status = "default"
    provider = ""
    region_id = 1


class UserProfileFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserProfileModel

    uuid = str(uuid.uuid4())
    file_name = "file"
    path = "uploads/"


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = PostModel

    title = "떡볶이 나눠 먹어요"
    region_group_id = 1
    type = "article"
    is_comment_disabled = False
    is_deleted = False
    is_blocked = False
    report_count = 0
    read_count = 0
    category = 0
    last_user_action = "default"
    last_admin_action = "default"
    user_id = 1

    @factory.post_generation
    def Article(obj, create, extracted, **kwargs):
        if extracted:
            ArticleFactory(post=obj, **kwargs)


class ArticleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ArticleModel

    body = factory.Sequence(lambda n: "body_{}".format(n))
    post_id = 1


class RegionGroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RegionGroupModel

    name = factory.Sequence(lambda n: "region_group_{}".format(n))


class RegionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RegionModel

    name = factory.Sequence(lambda n: "region_{}".format(n))

    region_group = factory.SubFactory(RegionGroupFactory)

    @factory.post_generation
    def RegionGroup(obj, create, extracted, **kwargs):
        if extracted:
            RegionGroupFactory(region=obj, **kwargs)
