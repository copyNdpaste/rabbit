from pydantic import BaseModel, ValidationError, StrictInt, StrictStr

from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto


class CreatePostSchema(BaseModel):
    user_id: StrictInt
    title: StrictStr
    body: StrictStr
    region_group_id: StrictInt
    type: StrictStr
    is_comment_disabled: bool
    is_deleted: bool
    is_blocked: bool
    report_count: StrictInt
    read_count: StrictInt
    category: StrictInt


class CreatePostRequest:
    def __init__(
        self,
        user_id,
        title,
        body,
        region_group_id,
        type,
        is_comment_disabled,
        is_deleted,
        is_blocked,
        report_count,
        read_count,
        category,
    ):
        self.user_id = user_id
        self.title = title
        self.body = body
        self.region_group_id = region_group_id
        self.type = type
        self.is_comment_disabled = is_comment_disabled
        self.is_deleted = is_deleted
        self.is_blocked = is_blocked
        self.report_count = report_count
        self.read_count = read_count
        self.category = category

    def validate_request_and_make_dto(self):
        try:
            CreatePostSchema(
                user_id=self.user_id,
                title=self.title,
                body=self.body,
                region_group_id=self.region_group_id,
                type=self.type,
                is_comment_disabled=self.is_comment_disabled,
                is_deleted=self.is_deleted,
                is_blocked=self.is_blocked,
                report_count=self.report_count,
                read_count=self.read_count,
                category=self.category,
            )
            return self.to_dto()
        except ValidationError as e:
            print(e)
            return False

    def to_dto(self) -> CreatePostDto:
        return CreatePostDto(
            user_id=self.user_id,
            title=self.title,
            body=self.body,
            region_group_id=self.region_group_id,
            type=self.type,
            is_comment_disabled=self.is_comment_disabled,
            is_deleted=self.is_deleted,
            is_blocked=self.is_blocked,
            report_count=self.report_count,
            read_count=self.read_count,
            category=self.category,
        )


class UpdatePostSchema(BaseModel):
    id: StrictInt
    user_id: StrictInt
    title: StrictStr
    body: StrictStr
    region_group_id: StrictInt
    type: StrictStr
    is_comment_disabled: bool
    category: StrictInt


class UpdatePostRequest:
    def __init__(
        self,
        id,
        user_id,
        title,
        body,
        region_group_id,
        type,
        is_comment_disabled,
        category,
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.body = body
        self.region_group_id = region_group_id
        self.type = type
        self.is_comment_disabled = is_comment_disabled
        self.category = category

    def validate_request_and_make_dto(self):
        try:
            UpdatePostSchema(
                id=self.id,
                user_id=self.user_id,
                title=self.title,
                body=self.body,
                region_group_id=self.region_group_id,
                type=self.type,
                is_comment_disabled=self.is_comment_disabled,
                category=self.category,
            )
            return self.to_dto()
        except ValidationError as e:
            print(e)
            return False

    def to_dto(self) -> UpdatePostDto:
        return UpdatePostDto(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            body=self.body,
            region_group_id=self.region_group_id,
            type=self.type,
            is_comment_disabled=self.is_comment_disabled,
            category=self.category,
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
        return DeletePostDto(id=self.post_id, user_id=self.user_id)
