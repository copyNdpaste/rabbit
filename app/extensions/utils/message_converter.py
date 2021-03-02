import uuid
from app.extensions.utils.time_helper import get_server_timestamp
from core.domains.notification.dto.notification_dto import MessageDto


class NotificationMessageConverter:
    @staticmethod
    def to_dict(dto: MessageDto):
        return {
            "uuid": str(uuid.uuid4()),
            "msg": {
                "post_id": dto.post_id,
                "user_id": dto.user_id,
                "category": dto.category,
                "type": dto.type,
                "message": dto.msg,
                "created_at": str(get_server_timestamp().replace(microsecond=0))
            },
        }
