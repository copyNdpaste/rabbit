from typing import Optional

import inject

from app.extensions.utils.event_observer import send_message, get_event_object
from core.domains.board.dto.post_like_dto import LikePostDto
from core.domains.board.enum import PostTopicEnum
from core.domains.board.enum.post_enum import PostLikeStateEnum
from core.domains.board.repository.board_repository import BoardRepository
from core.domains.user.entity.user_entity import UserEntity
from core.domains.user.enum import UserTopicEnum
from core.use_case_output import UseCaseFailureOutput, FailureType, UseCaseSuccessOutput


class LikePostUseCase:
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
        self._board_repo = board_repo

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
            self._board_repo.create_post_like_state(
                user_id=dto.user_id, post_id=dto.post_id
            )
        else:
            to_be_adopted_post_like_state = self._get_to_be_adopted_post_like_state(
                state=post_like_state.state
            )

            self._board_repo.update_post_like_state(
                user_id=dto.user_id,
                post_id=dto.post_id,
                state=to_be_adopted_post_like_state,
            )
        post_like_state = self._board_repo.get_post_like_state(
            user_id=dto.user_id, post_id=dto.post_id
        )

        return UseCaseSuccessOutput(value=post_like_state)

    def _get_user(self, user_id: int) -> Optional[UserEntity]:
        send_message(UserTopicEnum.GET_USER, user_id=user_id)

        return get_event_object(UserTopicEnum.GET_USER)

    def _is_post_exist(self, post_id) -> bool:
        send_message(PostTopicEnum.IS_POST_EXIST, post_id=post_id)

        return get_event_object(topic_name=PostTopicEnum.IS_POST_EXIST)

    def _get_to_be_adopted_post_like_state(self, state: str) -> str:
        return (
            PostLikeStateEnum.UNLIKE.value
            if state == PostLikeStateEnum.LIKE.value
            else PostLikeStateEnum.LIKE.value
        )
