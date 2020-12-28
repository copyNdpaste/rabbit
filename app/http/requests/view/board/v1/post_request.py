from pydantic import BaseModel, ValidationError

from core.domains.board.dto.post_dto import CreatePostDto


class CreatePostSchema(BaseModel):
    user_id: int
    title: str
    region_group_id: str
    type: str
    is_comment_disabled: bool
    is_deleted: bool
    is_blocked: bool
    report_count: int
    read_count: int
    category: int


class CreatePostRequest:
    def __init__(
        self,
        user_id,
        title,
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
            region_group_id=self.region_group_id,
            type=self.type,
            is_comment_disabled=self.is_comment_disabled,
            is_deleted=self.is_deleted,
            is_blocked=self.is_blocked,
            report_count=self.report_count,
            read_count=self.read_count,
            category=self.category,
        )
