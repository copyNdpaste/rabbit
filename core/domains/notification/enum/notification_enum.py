from enum import Enum


class CategoryEnum(Enum):
    KEYWORD = "bium1"
    CHAT = "bium2"


class TypeEnum(Enum):
    IN = "in"
    OUT = "out"
    ALL = "all"


class StatusEnum(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAIL = "fail"


class TitleEnum(Enum):
    KEYWORD = "키워드 알림"
    CHAT = "채팅 알림"


class BodyEnum(Enum):
    KEYWORD = "키워드 등록한 물품이 게시되었습니다."
    CHAT = "메세지가 왔습니다."


class RedisExpire(Enum):
    TIME = 600


class RedisKeyPrefix(Enum):
    KEYWORD = "keyword"
