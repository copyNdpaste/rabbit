from enum import Enum


class PostLimitEnum(Enum):
    LIMIT = 10


class PostCategoryEnum(Enum):
    DIVIDING_FOOD_INGREDIENT = "dividing_food_ingredient"  # 식자재 나누기. id 1
    DIVIDING_NECESSITIES = "dividing_necessities"  # 생필품 나누기. id 2
    LOST_MISSING = "lost_missing"  # 분실/실종. id 3
    USED_TRADING = "used_trading"  # 중고거래. id 4

    @staticmethod
    def get_list():
        return list(map(lambda c: c.value, PostCategoryEnum))


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
