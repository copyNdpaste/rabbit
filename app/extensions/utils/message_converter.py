import uuid
from app.extensions.utils.time_helper import get_server_timestamp
from core.domains.notification.dto.notification_dto import MessageDto


class NotificationMessageConverter:
    @staticmethod
    def to_dict(dto: MessageDto):
        return {
            "message": {
                "uuid": str(uuid.uuid4()),
                "token": dto.token,
                "category": dto.category,
                "type": dto.type,
                "notification": {
                    "title": dto.title,
                    "body": dto.body,
                },
                "data": {
                    "post_id": dto.post_id,
                    "user_id": dto.user_id,
                    "created_at": str(get_server_timestamp().replace(microsecond=0))
                }
            }
        }
