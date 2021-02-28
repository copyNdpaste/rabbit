import os
import uuid
import inject
from typing import Union, Optional
from app.extensions.utils.enum.aws_enum import S3BucketEnum, S3PathEnum
from app.extensions.utils.event_observer import send_message, get_event_object
from app.extensions.utils.image_helper import S3Helper
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
from core.domains.board.enum import PostTopicEnum
from core.domains.board.enum.attachment_enum import AttachmentEnum
from core.domains.board.enum.post_enum import PostLikeStateEnum, PostLikeCountEnum
from core.domains.board.repository.board_repository import BoardRepository
from core.domains.region.enum import RegionTopicEnum
from core.domains.user.entity.user_entity import UserEntity
from core.domains.user.enum import UserTopicEnum
from core.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput, FailureType


class PostBaseUseCase:
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
        self._board_repo = board_repo

    def _get_user(self, user_id: int) -> Optional[UserEntity]:
        send_message(UserTopicEnum.GET_USER, user_id=user_id)

        return get_event_object(UserTopicEnum.GET_USER)

    def _is_post_owner(self, dto):
        return self._board_repo.is_post_owner(dto=dto)

    def _make_cursor(self, last_post_id: int = None) -> dict:
        return {"cursor": {"last_post_id": last_post_id}}

    def _upload_pictures(self, dto, post_id: int):
        attachment_list = []

        for file in dto.files:
            f, extension = os.path.splitext(file.filename)
            uuid_ = str(uuid.uuid4())
            object_name = S3PathEnum.POST_IMGS.value + uuid_ + extension

            res = S3Helper.upload(
                bucket=S3BucketEnum.LUDICER_BUCKET.value,
                file_name=file,
                object_name=object_name,
            )

            if not res:
                return False

            attachment = self._board_repo.create_attachment(
                post_id=post_id,
                type=dto.type,
                file_name=f,
                path=S3PathEnum.POST_IMGS.value,
                extension=extension,
                uuid=uuid_,
            )
            if not attachment:
                return False
            attachment_list.append(object_name)

        return attachment_list


class CreatePostUseCase(PostBaseUseCase):
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
        super().__init__(board_repo)
        self._board_repo = board_repo

    def execute(
        self, dto: CreatePostDto
    ) -> Union[UseCaseSuccessOutput, UseCaseFailureOutput]:
        user = self._get_user(dto.user_id)
        if not user:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        post = self._board_repo.create_post(dto=dto)
        if not post:
            return UseCaseFailureOutput(type=FailureType.SYSTEM_ERROR)

        attachments = []
        if dto.file_type == AttachmentEnum.PICTURE.value:
            attachments = self._upload_pictures(dto=dto, post_id=post.id)
            if attachments == False:
                return UseCaseFailureOutput(type=FailureType.SYSTEM_ERROR)

        post_like_count = self._board_repo.create_post_like_count(post_id=post.id)
        if not post_like_count:
            return UseCaseFailureOutput(type=FailureType.SYSTEM_ERROR)

        post.post_like_count = post_like_count.count
        post.attachments = attachments

        return UseCaseSuccessOutput(value=post)


class GetPostListUseCase(PostBaseUseCase):
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
        super().__init__(board_repo)
        self._board_repo = board_repo

    def execute(
        self, dto: GetPostListDto
    ) -> Union[UseCaseSuccessOutput, UseCaseFailureOutput]:
        is_region_group_exist = self._get_region_group(id=dto.region_group_id)
        if not is_region_group_exist:
            return UseCaseFailureOutput(FailureType.NOT_FOUND_ERROR)

        post_list = self._board_repo.get_post_list(
            region_group_id=dto.region_group_id,
            previous_post_id=dto.previous_post_id,
            title=dto.title,
            category_ids=dto.category_ids,
            status=dto.status,
        )

        return UseCaseSuccessOutput(
            value=post_list,
            meta=self._make_cursor(
                last_post_id=post_list[-1].id if post_list else None
            ),
        )

    def _get_region_group(self, id: int):
        send_message(topic_name=RegionTopicEnum.GET_REGION_GROUP, id=id)

        return get_event_object(topic_name=RegionTopicEnum.GET_REGION_GROUP)


class GetPostUseCase(PostBaseUseCase):
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
        super().__init__(board_repo)
        self._board_repo = board_repo

    def execute(self, dto: GetPostDto):
        post = self._board_repo.get_post(post_id=dto.post_id)
        if not post:
            return UseCaseFailureOutput(FailureType.NOT_FOUND_ERROR)
        try:
            self._board_repo.add_read_count(post_id=dto.post_id)
        except Exception as e:
            # TODO : 로그
            return UseCaseFailureOutput(FailureType.SYSTEM_ERROR)
        post = self._board_repo.get_post(post_id=dto.post_id)

        attachment_list = []
        if post and post.attachments:
            for attachment in post.attachments:
                attachment_list.append(
                    attachment.path + attachment.uuid + attachment.extension
                )
        post.attachments = attachment_list

        return UseCaseSuccessOutput(value=post)


class UpdatePostUseCase(PostBaseUseCase):
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
        super().__init__(board_repo)
        self._board_repo = board_repo

    def execute(
        self, dto: UpdatePostDto
    ) -> Union[UseCaseSuccessOutput, UseCaseFailureOutput]:
        is_post_owner = self._is_post_owner(dto=dto)
        if not is_post_owner:
            return UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)

        post = self._board_repo.update_post(dto=dto)
        if not post:
            return UseCaseFailureOutput(type=FailureType.SYSTEM_ERROR)

        attachments = self._board_repo.get_attachments(post_id=post.id)
        if attachments:
            self._board_repo.delete_attachments(post_id=post.id)
        attachments = []
        if dto.file_type == AttachmentEnum.PICTURE.value:
            attachments = self._upload_pictures(dto=dto, post_id=post.id)
            if attachments == False:
                return UseCaseFailureOutput(type=FailureType.SYSTEM_ERROR)
        post.attachments = attachments

        return UseCaseSuccessOutput(value=post)


class DeletePostUseCase(PostBaseUseCase):
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
        super().__init__(board_repo)
        self._board_repo = board_repo

    def execute(
        self, dto: DeletePostDto
    ) -> Union[UseCaseSuccessOutput, UseCaseFailureOutput]:
        is_post_owner = self._is_post_owner(dto=dto)
        if not is_post_owner:
            return UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)

        post = self._board_repo.delete_post(dto=dto)
        if not post:
            return UseCaseFailureOutput(type=FailureType.SYSTEM_ERROR)
        return UseCaseSuccessOutput(value=post)


class LikePostUseCase(PostBaseUseCase):
    def execute(self, dto: LikePostDto):
        user = self._get_user(dto.user_id)
        if not user:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        is_post_exist = self._is_post_exist(post_id=dto.post_id)
        if not is_post_exist:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        post_like_state = self._board_repo.get_post_like_state(
            user_id=dto.user_id, post_id=dto.post_id
        )
        if not post_like_state:
            post_like_state = self._board_repo.create_post_like_state(
                user_id=dto.user_id, post_id=dto.post_id
            )
            if not post_like_state:
                return UseCaseFailureOutput(FailureType.SYSTEM_ERROR)

            post_like_count = self._board_repo.update_post_like_count(
                post_id=dto.post_id, count=PostLikeCountEnum.UP.value
            )
            if not post_like_count:
                return UseCaseFailureOutput(FailureType.SYSTEM_ERROR)
        else:
            state = post_like_state.state
            to_be_adopted_post_like_state = self._get_to_be_adopted_post_like_state(
                state=state
            )

            post_like_state = self._board_repo.update_post_like_state(
                user_id=dto.user_id,
                post_id=dto.post_id,
                state=to_be_adopted_post_like_state,
            )
            if not post_like_state:
                return UseCaseFailureOutput(FailureType.SYSTEM_ERROR)

            post_like_count = self._update_post_like_count(state=state, dto=dto)
            if not post_like_count:
                return UseCaseFailureOutput(FailureType.SYSTEM_ERROR)

            post_like_state = self._board_repo.get_post_like_state(
                user_id=dto.user_id, post_id=dto.post_id
            )

        post = self._board_repo.get_post(post_id=dto.post_id)
        post.post_like_state = post_like_state.state

        return UseCaseSuccessOutput(value=post)

    def _is_post_exist(self, post_id) -> bool:
        send_message(PostTopicEnum.IS_POST_EXIST, post_id=post_id)

        return get_event_object(topic_name=PostTopicEnum.IS_POST_EXIST)

    def _get_to_be_adopted_post_like_state(self, state: str) -> str:
        return (
            PostLikeStateEnum.UNLIKE.value
            if state == PostLikeStateEnum.LIKE.value
            else PostLikeStateEnum.LIKE.value
        )

    def _get_to_be_up_or_down_count(self, state: str) -> int:
        return (
            PostLikeCountEnum.DOWN.value
            if state == PostLikeStateEnum.LIKE.value
            else PostLikeCountEnum.UP.value
        )

    def _update_post_like_count(self, state: str, dto) -> bool:
        to_be_up_or_down_count = self._get_to_be_up_or_down_count(state=state)
        return self._board_repo.update_post_like_count(
            post_id=dto.post_id, count=to_be_up_or_down_count
        )


class GetSellingPostListUseCase(PostBaseUseCase):
    def execute(self, dto: GetSellingPostListDto):
        user = self._get_user(dto.user_id)
        if not user:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        selling_post_list = self._board_repo.get_selling_post_list(
            user_id=dto.user_id, previous_post_id=dto.previous_post_id
        )

        return UseCaseSuccessOutput(
            value=selling_post_list,
            meta=self._make_cursor(
                last_post_id=selling_post_list[-1].id if selling_post_list else None
            ),
        )


class GetLikePostListUseCase(PostBaseUseCase):
    def execute(self, dto: GetLikePostListDto):
        user = self._get_user(dto.user_id)
        if not user:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        like_post_list = self._board_repo.get_like_post_list(
            user_id=dto.user_id, previous_post_id=dto.previous_post_id
        )

        return UseCaseSuccessOutput(
            value=like_post_list,
            meta=self._make_cursor(
                last_post_id=like_post_list[-1].id if like_post_list else None
            ),
        )
