from typing import Union

import inject

from app.extensions.utils.event_observer import send_message, get_event_object
from core.domains.board.dto.post_dto import CreatePostDto
from core.domains.board.repository.board_repository import BoardRepository
from core.domains.user.entity.user_entity import UserEntity
from core.domains.user.enum import UserTopicEnum
from core.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput, FailureType


class CreatePostUseCase:
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
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

    def _get_user(self, user_id: int) -> Union[UserEntity, bool]:
        send_message(UserTopicEnum.GET_USER, user_id=user_id)

        return get_event_object(UserTopicEnum.GET_USER)
