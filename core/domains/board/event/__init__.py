from flask import g
from pubsub import pub

from core.domains.board.enum import PostTopicEnum
from core.domains.board.repository.board_repository import BoardRepository


def is_post_exist(post_id: int):
    is_exist = BoardRepository().is_post_exist(post_id=post_id)

    setattr(g, PostTopicEnum.IS_POST_EXIST, is_exist)


pub.subscribe(is_post_exist, PostTopicEnum.IS_POST_EXIST)
