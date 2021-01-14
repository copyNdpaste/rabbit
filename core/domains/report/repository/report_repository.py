from typing import Optional

from app.extensions.database import session
from app.persistence.model.post_report_model import PostReportModel
from core.domains.board.entity.report_entity import PostReportEntity
from core.domains.report.dto.post_report_dto import CreatePostReportDto


class ReportRepository:
    def create_post_report(
        self, dto: CreatePostReportDto
    ) -> Optional[PostReportEntity]:
        try:
            post_report = PostReportModel(
                post_id=dto.post_id,
                report_user_id=dto.report_user_id,
                status=dto.status,
                context=dto.status,
                confirm_admin_id=dto.confirm_admin_id,
                is_system_report=dto.is_system_report,
            )
            session.add(post_report)
            session.commit()

            return post_report
        except Exception as e:
            # TODO : log
            session.rollback()
            return None
