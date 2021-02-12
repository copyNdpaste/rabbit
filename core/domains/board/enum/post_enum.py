from enum import Enum


class PostLimitEnum(Enum):
    LIMIT = 10


class PostCategoryEnum(Enum):
    DIVIDING_FOOD_INGREDIENT = 1  # 식자재 나누기. id 1
    DIVIDING_NECESSITIES = 2  # 생필품 나누기. id 2
    LOST_MISSING = 3  # 분실/실종. id 3
    USED_TRADING = 4  # 중고거래. id 4

    @staticmethod
    def get_dict():
        dct = {}
        for e in PostCategoryEnum:
            dct[e.value] = e.name.lower()
        return dct


class PostUnitEnum(Enum):
    UNIT = "unit"  # 개
    BOTTLE = "bottle"  # 병
    DIRECT_INPUT = "direct_input"  # 직접입력


class PostStatusEnum(Enum):
    SELLING = "selling"  # 판매중
    RESERVATION = "reservation"  # 예약중
    COMPLETED = "completed"  # 거래완료


class PostLikeStateEnum(Enum):
    LIKE = "like"
    UNLIKE = "unlike"
    DEFAULT = "default"


class PostLikeCountEnum(Enum):
    DEFAULT = 0
    UP = 1
    DOWN = -1
