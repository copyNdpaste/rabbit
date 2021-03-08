from typing import Optional

import inject

from app.extensions.utils.event_observer import send_message, get_event_object
from core.domains.board.entity.post_entity import PostEntity
from core.domains.board.enum import PostTopicEnum
from core.domains.report.dto.post_report_dto import CreatePostReportDto
from core.domains.report.enum.report_enum import PostReportEnum
from core.domains.report.repository.report_repository import ReportRepository
from core.use_case_output import UseCaseFailureOutput, FailureType, UseCaseSuccessOutput


class CreatePostReportUseCase:
    @inject.autoparams()
    def __init__(self, report_repo: ReportRepository):
        self.report_repo = report_repo

    def execute(self, dto: CreatePostReportDto):
        is_post_exist = self._is_post_exist(post_id=dto.post_id)
        if not is_post_exist:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        post_report = self.report_repo.get_post_report(
            report_user_id=dto.report_user_id, post_id=dto.post_id
        )
        if post_report:
            return UseCaseFailureOutput(type=FailureType.ALREADY_EXIST)

        post_report = self.report_repo.create_post_report(dto=dto)
        if not post_report:
            return UseCaseFailureOutput(type=FailureType.SYSTEM_ERROR)

        post_report_count = self._add_report_count(post_id=dto.post_id)

        if post_report_count >= PostReportEnum.REPORT_MAX_COUNT.value:
            self._block_post(post_id=dto.post_id)

        return UseCaseSuccessOutput(value=post_report)

    def _is_post_exist(self, post_id: int) -> bool:
        send_message(topic_name=PostTopicEnum.IS_POST_EXIST.value, post_id=post_id)

        return get_event_object(topic_name=PostTopicEnum.IS_POST_EXIST.value)

    def _add_report_count(self, post_id: int) -> int:
        send_message(topic_name=PostTopicEnum.ADD_REPORT_COUNT.value, post_id=post_id)

        return get_event_object(topic_name=PostTopicEnum.ADD_REPORT_COUNT.value)

    def _block_post(self, post_id: int):
        send_message(topic_name=PostTopicEnum.BLOCK.value, post_id=post_id)

        return get_event_object(topic_name=PostTopicEnum.BLOCK.value)
