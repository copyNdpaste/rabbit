from typing import List

from pydantic import BaseModel, ValidationError, StrictInt, StrictStr
from core.domains.user.dto.user_dto import GetUserDto, UpdateUserDto


class GetUserSchema(BaseModel):
    user_id: int


class GetUserRequest:
    def __init__(self, user_id):
        self.user_id = int(user_id) if user_id else None

    def validate_request_and_make_dto(self):
        try:
            schema = GetUserSchema(user_id=self.user_id).dict()
            return GetUserDto(**schema)
        except ValidationError as e:
            print(e)
            return False


class UpdateUserSchema(BaseModel):
    user_id: StrictInt
    nickname: StrictStr
    status: StrictStr
    region_id: StrictInt
    files: List = []


class UpdateUserRequest:
    def __init__(self, user_id, nickname, status, region_id, files):
        self.user_id = int(user_id) if user_id else None
        self.nickname = nickname
        self.status = status
        self.region_id = int(region_id) if region_id else None
        self.files = files

    def validate_request_and_make_dto(self):
        try:
            schema = UpdateUserSchema(
                user_id=self.user_id,
                nickname=self.nickname,
                status=self.status,
                region_id=self.region_id,
                files=self.files,
            ).dict()
            return UpdateUserDto(**schema)
        except ValidationError as e:
            print(e)
            return False
