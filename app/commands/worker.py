import click
from flask import current_app

from app.commands.enum import TopicEnum
from core.domains.notification.use_case.v1.notification_use_case import (
    NotificationUseCase,
)


def get_worker(topic: str):
    if topic == TopicEnum.SEND_KEYWORD_NOTIFICATION.value:
        return NotificationUseCase(topic=topic)


@current_app.cli.command("start-worker")
@click.argument("topic")
def start_worker(topic):
    us = get_worker(topic)
    us.execute()
