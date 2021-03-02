import inject

from core.domains.board.repository.board_repository import BoardRepository
from core.domains.notification.repository.notification_repository import NotificationRepository
from core.domains.report.repository.report_repository import ReportRepository
from core.domains.user.repository.user_repository import UserRepository


def init_provider():
    inject.clear_and_configure(
        lambda binder: binder.bind_to_provider(UserRepository, UserRepository)
    )
    inject.clear_and_configure(
        lambda binder: binder.bind_to_provider(BoardRepository, BoardRepository)
    )
    inject.clear_and_configure(
        lambda binder: binder.bind_to_provider(ReportRepository, ReportRepository)
    )
    inject.clear_and_configure(
        lambda binder: binder.bind_to_provider(NotificationRepository, NotificationRepository)
    )
