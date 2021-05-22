import json
import os
import sys
from time import sleep
from typing import Optional, List

from flask import current_app
from redis import Redis

from app import redis
from pyfcm import FCMNotification

from app.extensions.utils.event_observer import send_message

from core.domains.notification.enum import NotificationTopicEnum
from core.domains.notification.enum.notification_enum import StatusEnum


class NotificationUseCase:
    def __init__(self, topic: str, redis_client: Optional[Redis] = None):
        self.topic = topic
        self.redis = redis_client or redis
        self.push_service = FCMNotification(api_key=current_app.config.get("FCM_KEY"))

        if not hasattr(self, "stdout"):
            self.stdout = sys.stdout

        if not hasattr(self, "stderr"):
            self.stderr = sys.stderr

    def execute(self):
        self.stdout.write(f"🚀\tSTARTING NOTIFICATION SEND - {self.client_id}")
        self.stdout.write(f"\n🚀\tFCM KEY - {current_app.config.get('FCM_KEY')}")
        while True:
            self.redis.scan_pattern(pattern="keyword*")

            # 3분마다 실행
            sleep(180)
            messages = self._get_messages()
            self._logging(message=f"\n[*] Get keyword data -> {len(messages)}")

            self._push_notification(messages)

            # Clear cache
            if self.redis.copied_keys:
                self._logging(message=f"[*] Clear keys -> {self.redis.copied_keys}")
                self.redis.clear_cache()

    def _get_messages(self) -> List:
        result = dict()
        messages = list()
        while True:
            try:
                data = self.redis.get_after_scan()
                if data is None:
                    break
                result[data["key"].decode().split(":")[1]] = json.loads(data["value"])
                messages.append(result)
            except Exception as e:
                self._logging(message="[*] _get_messages() exception")
                self._logging(message=str(e))
                break
        return messages

    def _push_notification(self, messages: List[dict]):
        try:
            for message in messages:
                for key in message:
                    response = self.push_service.notify_single_device(
                        registration_id=message[key].get("message").get("token"),
                        data_message=message[key],
                    )
                    self._logging(
                        message=f"[*] FCM response -> {response.get('success')}"
                    )

                    # notification_history 상태값 변경
                    status = StatusEnum.SUCCESS.value
                    if response.get("failure") > 0:
                        status = StatusEnum.FAIL.value

                    self._update_notification_status(
                        notification_history_id=key, status=status
                    )
        except Exception as e:
            self._logging(message="[*] _push_notification() exception")
            self._logging(message=str(e))

    def _update_notification_status(self, notification_history_id: int, status: str):
        send_message(
            topic_name=NotificationTopicEnum.UPDATE_NOTIFICATION_STATUS,
            notification_history_id=notification_history_id,
            status=status,
        )

    def _logging(self, message: str) -> None:
        print(message)

    @property
    def client_id(self) -> str:
        return f"{self.topic}-{os.getpid()}"
