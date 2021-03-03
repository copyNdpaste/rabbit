import json
from typing import Optional

from redis import Redis

from app import redis
from app.extensions.database import session
from app.persistence.model.notification_history_model import NotificationHistoryModel
from core.domains.notification.dto.notification_dto import NotificationHistoryDto
from core.domains.notification.enum.notification_enum import RedisExpire, RedisKeyPrefix


class NotificationRepository:
    def __init__(self, redis_client: Optional[Redis] = None):
        self.redis = redis_client or redis

    def create_notification_history(self, dto: NotificationHistoryDto) -> None:
        try:
            notification_history = NotificationHistoryModel(
                user_id=dto.user_id,
                status=dto.status,
                type=dto.type,
                category=dto.category,
                message=dto.message,
            )
            session.add(notification_history)
            session.commit()

            self._set_notification_info(notification_history.id, dto.message)

        except Exception as e:
            # TODO : log e 필요
            session.rollback()

    def _set_notification_info(self, notification_history_id: int, message: dict) -> None:
        self.redis.set(
            key=f"{RedisKeyPrefix.KEYWORD.value}:{str(notification_history_id)}",
            value=json.dumps(message, ensure_ascii=False).encode('UTF-8'),
            ex=RedisExpire.TIME.value
        )