from typing import List

from flask import g
from pubsub import pub

from core.domains.notification.dto.notification_dto import NotificationHistoryDto
from core.domains.notification.enum import NotificationTopicEnum
from core.domains.notification.repository.notification_repository import (
    NotificationRepository,
)


def get_keyword_target_user():
    target_user_groups = NotificationRepository().get_keyword_target_user()

    setattr(g, NotificationTopicEnum.GET_KEYWORD_TARGET_USER, target_user_groups)


def create_notification_history(notification_list: List[NotificationHistoryDto]):
    NotificationRepository().create_notification_history(
        notification_list=notification_list
    )


def update_notification_status(notification_history_id: int, status: str):
    NotificationRepository().update_notification_status(
        notification_history_id=notification_history_id, status=status
    )


pub.subscribe(get_keyword_target_user, NotificationTopicEnum.GET_KEYWORD_TARGET_USER)
pub.subscribe(
    create_notification_history, NotificationTopicEnum.CREATE_NOTIFICATION_HISTORY
)
pub.subscribe(
    update_notification_status, NotificationTopicEnum.UPDATE_NOTIFICATION_STATUS
)
