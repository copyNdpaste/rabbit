import json
from typing import Optional, List

from redis import Redis

from app import redis
from app.extensions.database import session
from app.persistence.model.keyword_model import KeywordModel
from app.persistence.model.notification_history_model import NotificationHistoryModel
from app.persistence.model.notification_model import NotificationModel
from app.persistence.model.user_notification_token_model import (
    UserNotificationTokenModel,
)
from core.domains.notification.dto.notification_dto import (
    NotificationHistoryDto,
    KeywordTargetUserDto,
)
from core.domains.notification.enum.notification_enum import RedisExpire, RedisKeyPrefix


class NotificationRepository:
    def __init__(self, redis_client: Optional[Redis] = None):
        self.redis = redis_client or redis

    def create_notification_history(
        self, notification_list: List[NotificationHistoryDto]
    ) -> None:
        try:
            for dto in notification_list:
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
            print("-------------------> ", e)
            session.rollback()

    def _set_notification_info(
        self, notification_history_id: int, message: dict
    ) -> None:
        self.redis.set(
            key=f"{RedisKeyPrefix.KEYWORD.value}:{str(notification_history_id)}",
            value=json.dumps(message, ensure_ascii=False).encode("UTF-8"),
            ex=RedisExpire.TIME.value,
        )

    def get_keyword_target_user(self) -> List[dict]:
        target_user_group = (
            session.query(NotificationModel)
            .with_entities(
                NotificationModel.user_id,
                UserNotificationTokenModel.token,
                KeywordModel.name_1,
                KeywordModel.name_2,
                KeywordModel.name_3,
            )
            .join(
                UserNotificationTokenModel,
                NotificationModel.user_id == UserNotificationTokenModel.user_id,
            )
            .join(KeywordModel, NotificationModel.user_id == KeywordModel.user_id)
            .filter(
                NotificationModel.is_available == True,
                NotificationModel.use_keyword == True,
            )
            .all()
        )

        result = []
        for target_user in target_user_group:
            info_dict = dict(
                user_id=target_user.user_id,
                token=target_user.token,
                keyword_1=target_user.name_1,
                keyword_2=target_user.name_2,
                keyword_3=target_user.name_3,
            )
            result.append(info_dict)
        return result

    def update_notification_status(
        self, notification_history_id: int, status: str
    ) -> None:
        try:
            session.query(NotificationHistoryModel).filter_by(
                id=notification_history_id
            ).update({"status": status})
        except Exception as e:
            # TODO : log e 필요
            print("-------------------> ", e)
            session.rollback()
