import json
from typing import List
from pydantic import BaseModel, ValidationError, StrictInt, StrictStr
from core.domains.board.dto.post_dto import (
    CreatePostDto,
    UpdatePostDto,
    DeletePostDto,
    GetPostListDto,
    GetPostDto,
    GetSellingPostListDto,
    GetLikePostListDto,
)
from core.domains.board.dto.post_like_dto import LikePostDto


class CreatePostSchema(BaseModel):
    user_id: StrictInt
    title: StrictStr
    body: StrictStr
    region_group_id: StrictInt
    type: StrictStr
    is_comment_disabled: bool
    category_ids: List[int]
    amount: StrictInt
    unit: StrictStr
    price_per_unit: StrictInt
    status: StrictStr
    file_type: StrictStr
    files: List


# TODO : pydantic 활용해서 request 스키마 검증, dto 생성 간소화
class CreatePostRequest:
    def __init__(
        self,
        user_id,
        title,
        body,
        region_group_id,
        type,
        is_comment_disabled,
        category_ids,
        amount,
        unit,
        price_per_unit,
        status,
        file_type,
        files,
    ):
        self.user_id = int(user_id) if user_id else None
        self.title = title
        self.body = body
        self.region_group_id = int(region_group_id) if region_group_id else None
        self.type = type
        self.is_comment_disabled = (
            True if is_comment_disabled and is_comment_disabled == "true" else False
        )
        self.category_ids = json.loads(category_ids) if category_ids else []
        self.amount = int(amount) if amount else None
        self.unit = unit
        self.price_per_unit = int(price_per_unit) if price_per_unit else None
        self.status = status
        self.file_type = file_type
        self.files = files

    def validate_request_and_make_dto(self):
        try:
            schema = CreatePostSchema(
                user_id=self.user_id,
                title=self.title,
                body=self.body,
                region_group_id=self.region_group_id,
                type=self.type,
                is_comment_disabled=self.is_comment_disabled,
                category_ids=self.category_ids,
                amount=self.amount,
                unit=self.unit,
                price_per_unit=self.price_per_unit,
                status=self.status,
                file_type=self.file_type,
                files=self.files,
            ).dict()
            return CreatePostDto(**schema)
        except ValidationError as e:
            print(e)
            return False


class GetPostListSchema(BaseModel):
    region_group_id: StrictInt
    previous_post_id: StrictInt = None
    title: StrictStr = None
    type: StrictStr = None
    category_ids: List[int]
    status: str


class GetPostListRequest:
    def __init__(
        self,
        region_group_id,
        previous_post_id=None,
        title=None,
        type=None,
        category_ids=None,
        status=None,
    ):
        self.region_group_id = region_group_id
        self.previous_post_id = previous_post_id
        self.title = title
        self.type = type
        self.category_ids = category_ids
        self.status = status

    def validate_request_and_make_dto(self):
        try:
            GetPostListSchema(
                region_group_id=self.region_group_id,
                previous_post_id=self.previous_post_id,
                title=self.title,
                type=self.type,
                category_ids=self.category_ids,
                status=self.status,
            )
            return self.to_dto()
        except ValidationError as e:
            print(e)
            return False

    def to_dto(self) -> GetPostListDto:
        return GetPostListDto(
            region_group_id=self.region_group_id,
            previous_post_id=self.previous_post_id,
            title=self.title,
            type=self.type,
            category_ids=self.category_ids,
            status=self.status,
        )


class GetPostSchema(BaseModel):
    post_id: StrictInt


class GetPostRequest:
    def __init__(self, post_id):
        self.post_id = post_id

    def validate_request_and_make_dto(self):
        try:
            GetPostSchema(post_id=self.post_id)
            return self.to_dto()
        except ValidationError as e:
            print(e)
            return False

    def to_dto(self) -> GetPostDto:
        return GetPostDto(post_id=self.post_id)


class UpdatePostSchema(BaseModel):
    post_id: StrictInt
    user_id: StrictInt
    title: StrictStr
    body: StrictStr
    region_group_id: StrictInt
    type: StrictStr
    is_comment_disabled: bool
    category_ids: List[int]
    amount: StrictInt
    unit: StrictStr
    price_per_unit: StrictInt
    status: StrictStr


class UpdatePostRequest:
    def __init__(
        self,
        post_id,
        user_id,
        title,
        body,
        region_group_id,
        type,
        is_comment_disabled,
        category_ids,
        amount,
        unit,
        price_per_unit,
        status,
    ):
        self.post_id = post_id
        self.user_id = user_id
        self.title = title
        self.body = body
        self.region_group_id = region_group_id
        self.type = type
        self.is_comment_disabled = is_comment_disabled
        self.category_ids = category_ids
        self.amount = amount
        self.unit = unit
        self.price_per_unit = price_per_unit
        self.status = status

    def validate_request_and_make_dto(self):
        try:
            UpdatePostSchema(
                post_id=self.post_id,
                user_id=self.user_id,
                title=self.title,
                body=self.body,
                region_group_id=self.region_group_id,
                type=self.type,
                is_comment_disabled=self.is_comment_disabled,
                category_ids=self.category_ids,
                amount=self.amount,
                unit=self.unit,
                price_per_unit=self.price_per_unit,
                status=self.status,
            )
            return self.to_dto()
        except ValidationError as e:
            print(e)
            return False

    def to_dto(self) -> UpdatePostDto:
        return UpdatePostDto(
            post_id=self.post_id,
            user_id=self.user_id,
            title=self.title,
            body=self.body,
            region_group_id=self.region_group_id,
            type=self.type,
            is_comment_disabled=self.is_comment_disabled,
            category_ids=self.category_ids,
            amount=self.amount,
            unit=self.unit,
            price_per_unit=self.price_per_unit,
            status=self.status,
        )


class DeletePostSchema(BaseModel):
    post_id: StrictInt
    user_id: StrictInt


class DeletePostRequest:
    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    def validate_request_and_make_dto(self):
        try:
            DeletePostSchema(post_id=self.post_id, user_id=self.user_id)
            return self.to_dto()
        except ValidationError as e:
            print(e)
            return False

    def to_dto(self) -> DeletePostDto:
        return DeletePostDto(post_id=self.post_id, user_id=self.user_id)


class LikePostSchema(BaseModel):
    post_id: StrictInt
    user_id: StrictInt


class LikePostRequest:
    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    def validate_request_and_make_dto(self):
        try:
            LikePostSchema(post_id=self.post_id, user_id=self.user_id)
            return self.to_dto()
        except ValidationError as e:
            print(e)
            return False

    def to_dto(self) -> LikePostDto:
        return LikePostDto(post_id=self.post_id, user_id=self.user_id)


class GetSellingPostListSchema(BaseModel):
    user_id: StrictInt = None
    previous_post_id: StrictInt = None


class GetSellingPostListRequest:
    def __init__(self, user_id=None, previous_post_id=None):
        self.user_id = int(user_id) if user_id else None
        self.previous_post_id = int(previous_post_id) if previous_post_id else None

    def validate_request_and_make_dto(self):
        try:
            schema = GetSellingPostListSchema(
                user_id=self.user_id, previous_post_id=self.previous_post_id
            ).dict()
            return GetSellingPostListDto(**schema)
        except ValidationError as e:
            print(e)
            return False


class GetLikePostListSchema(BaseModel):
    user_id: StrictInt = None
    previous_post_id: StrictInt = None


class GetLikePostListRequest:
    def __init__(self, user_id=None, previous_post_id=None):
        self.user_id = int(user_id) if user_id else None
        self.previous_post_id = int(previous_post_id) if previous_post_id else None

    def validate_request_and_make_dto(self):
        try:
            schema = GetLikePostListSchema(
                user_id=self.user_id, previous_post_id=self.previous_post_id
            ).dict()
            return GetLikePostListDto(**schema)
        except ValidationError as e:
            print(e)
            return False
