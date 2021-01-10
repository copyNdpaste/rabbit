from typing import Union, Optional

import inject

from app.extensions.utils.event_observer import send_message, get_event_object
from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.repository.board_repository import BoardRepository
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
