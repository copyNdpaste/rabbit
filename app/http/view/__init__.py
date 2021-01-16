from flask import Blueprint

api: Blueprint = Blueprint("api/rabbit", __name__)

from .authentication.v1.auth_view import *  # noqa isort:skip
from .user.v1.user_view import *  # noqa isort:skip
from .board.v1.post_view import *  # noqa isort:skip
from .report.v1.post_report_view import *  # noqa isort:skip
