import json
import os
import sys
from time import sleep
from typing import Optional, List

from redis import Redis

from app import redis


class NotificationUseCase:
    def __init__(self, topic: str, redis_client: Optional[Redis] = None):
        self.topic = topic
        self.redis = redis_client or redis

        if not hasattr(self, "stdout"):
            self.stdout = sys.stdout

        if not hasattr(self, "stderr"):
            self.stderr = sys.stderr

    def execute(self):
        self.stdout.write(f"🚀\tSTARTING NOTIFICATION SEND - {self.client_id}")
        self.redis.scan_pattern(pattern="keyword*")
        while True:
            # 5분마다 실행
            sleep(3)
            self.redis.scan_pattern(pattern="keyword*")

            keywords = self._get_keywords()
            self._logging(message=f"[*] Get keyword data -> {len(keywords)}")

            # Clear cache
            if self.redis.copied_keys:
                self._logging(message=f"[*] Clear keys -> {self.redis.copied_keys}")
                self.redis.clear_cache()

    def _get_keywords(self) -> List:
        keywords = []
        while True:
            try:
                data = self.redis.get_after_scan()
                if data is None:
                    break
                keywords.append(json.loads(data["value"]))
            except Exception as e:
                self._logging(message="[*] _get_keywords() exception")
                self._logging(message=str(e))
                break
        return keywords

    def _logging(self, message: str) -> None:
        print(message)

    @property
    def client_id(self) -> str:
        return f"{self.topic}-{os.getpid()}"
