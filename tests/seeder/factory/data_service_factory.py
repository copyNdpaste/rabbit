import factory

from . import (
    UserFactory,
    PostFactory,
    UserProfileFactory,
    RegionFactory,
)


class NormalUserFactory(UserFactory):
    """
    일반 유저 생성기
    Todo 참조되는 모델 이곳에 추가
    """

    @factory.post_generation
    def Post(obj, create, extracted, **kwargs):
        if extracted:
            PostFactory(user=obj, **kwargs)

    @factory.post_generation
    def UserProfile(obj, create, extracted, **kwargs):
        if extracted:
            UserProfileFactory(user=obj, **kwargs)

    @factory.post_generation
    def Region(obj, create, extracted, **kwargs):
        if extracted:
            RegionFactory(user=obj, **kwargs)