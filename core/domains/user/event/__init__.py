from flask import g
from pubsub import pub

from core.domains.user.enum import UserTopicEnum
from core.domains.user.repository.user_repository import UserRepository


def get_user(user_id: int):
    user = UserRepository().get_user(user_id=user_id)

    setattr(g, UserTopicEnum.GET_USER, user)


pub.subscribe(get_user, UserTopicEnum.GET_USER)
