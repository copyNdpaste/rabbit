from typing import Union

import inject

from core.domains.board.dto.post_dto import CreatePostDto
from core.domains.board.repository.board_repository import BoardRepository
from core.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput


class CreatePostUseCase:
    @inject.autoparams()
    def __init__(self, board_repo: BoardRepository):
        self._board_repo = board_repo

    def execute(
        self, dto: CreatePostDto
    ) -> Union[UseCaseSuccessOutput, UseCaseFailureOutput]:
        # TODO : check user
        # TODO : create post, return result
        pass
