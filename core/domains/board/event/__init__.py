from flask import g
from pubsub import pub

from core.domains.board.enum import PostTopicEnum
from core.domains.board.repository.board_repository import BoardRepository


def is_post_exist(post_id: int):
    is_exist = BoardRepository().is_post_exist(post_id=post_id)

    setattr(g, PostTopicEnum.IS_POST_EXIST.value, is_exist)


def add_report_count(post_id: int):
    post = BoardRepository().add_report_count(post_id=post_id)

    setattr(g, PostTopicEnum.ADD_REPORT_COUNT.value, post)


def block(post_id: int):
    is_blocked = BoardRepository().block(post_id=post_id)

    setattr(g, PostTopicEnum.BLOCK.value, is_blocked)


def get_post(post_id: int, is_blocked: bool = False, is_deleted: bool = False):
    post = BoardRepository().get_post(
        post_id=post_id, is_blocked=is_blocked, is_deleted=is_deleted
    )

    setattr(g, PostTopicEnum.GET_POST.value, post)


pub.subscribe(is_post_exist, PostTopicEnum.IS_POST_EXIST.value)
pub.subscribe(add_report_count, PostTopicEnum.ADD_REPORT_COUNT.value)
pub.subscribe(block, PostTopicEnum.BLOCK.value)
pub.subscribe(get_post, PostTopicEnum.GET_POST.value)
