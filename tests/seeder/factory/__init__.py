import factory
import uuid
from faker import Factory as FakerFactory
from app.persistence.model.article_model import ArticleModel
from app.persistence.model.keyword_model import KeywordModel
from app.persistence.model.notification_model import NotificationModel
from app.persistence.model.post_model import PostModel
from app.persistence.model.region_group_model import RegionGroupModel
from app.persistence.model.region_model import RegionModel
from app.persistence.model.user_model import UserModel
from app.persistence.model.user_notification_token_model import UserNotificationTokenModel
from app.persistence.model.user_profile_model import UserProfileModel
from app.persistence.model.post_like_state_model import PostLikeStateModel
from app.persistence.model.post_like_count_model import PostLikeCountModel
from app.persistence.model.post_category_model import PostCategoryModel
from app.persistence.model.category_model import CategoryModel
from app.persistence.model.attachment_model import AttachmentModel
from core.domains.board.enum.post_enum import (
    PostUnitEnum,
    PostStatusEnum,
    PostLikeStateEnum,
    PostCategoryEnum,
)
from core.domains.board.enum.attachment_enum import AttachmentEnum
from app.extensions.utils.enum.aws_enum import S3PathEnum

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
    path = S3PathEnum.PROFILE_IMGS.value
    extension = ".jpg"


class PostLikeCountFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = PostLikeCountModel

    post_id = 1
    count = 0


class PostLikeStateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = PostLikeStateModel

    post_id = 1
    user_id = 1
    state = PostLikeStateEnum.LIKE.value


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CategoryModel

    id = 1
    name = PostCategoryEnum.DIVIDING_FOOD_INGREDIENT


class AttachmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AttachmentModel

    post_id = 1
    type = AttachmentEnum.PICTURE.value
    uuid = str(uuid.uuid4())
    file_name = factory.Sequence(lambda n: "file_name_{}".format(n))
    path = S3PathEnum.POST_IMGS.value
    extension = ".jpg"


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
    last_user_action = "default"
    last_admin_action = "default"
    user_id = 1
    amount = 0
    unit = PostUnitEnum.UNIT.value
    price_per_unit = 10000
    status = PostStatusEnum.SELLING.value

    @factory.post_generation
    def Article(obj, create, extracted, **kwargs):
        if extracted:
            ArticleFactory(post=obj, **kwargs)

    @factory.post_generation
    def PostLikeCount(obj, create, extracted, **kwargs):
        if extracted:
            PostLikeCountFactory(post=obj, **kwargs)

    @factory.post_generation
    def Categories(obj, create, extracted, **kwargs):
        if extracted:
            for category in extracted:
                obj.categories.append(category)

    @factory.post_generation
    def Attachments(self, create, extracted, **kwargs):
        if extracted:
            for attachment in extracted:
                self.attachments.append(attachment)


class PostCategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = PostCategoryModel

    post_id = 1
    category_id = 1


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


class NotificationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = NotificationModel

    user_id = 1
    is_available = True
    use_bantime = False
    use_keyword = True
    use_chat = True
    use_etc = True


class KeywordFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = KeywordModel

    user_id = 1
    name_1 = "양파"
    name_2 = "TEST"
    name_3 = "사과"


class UserNotificationTokenFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserNotificationTokenModel

    user_id = 1
    token = faker.bothify(text='????-#######')
