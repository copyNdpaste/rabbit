from typing import List
from pydantic import BaseModel, StrictInt, StrictStr


class GetUserDto(BaseModel):
    user_id: StrictInt


class UpdateUserDto(BaseModel):
    user_id: StrictInt
    nickname: StrictStr
    status: StrictStr
    region_id: StrictInt
    files: List = []
