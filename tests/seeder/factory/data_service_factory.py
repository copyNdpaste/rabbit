import factory

from . import UserFactory, PostFactory


class NormalUserFactory(UserFactory):
    """
    일반 유저 생성기
    Todo 참조되는 모델 이곳에 추가
    """

    @factory.post_generation
    def Post(obj, create, extracted, **kwargs):
        if extracted:
            PostFactory(user=obj, **kwargs)
