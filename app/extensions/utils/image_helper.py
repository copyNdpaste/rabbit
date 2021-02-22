import os
import uuid

import boto3
import inject
from botocore.exceptions import ClientError

from app.extensions.utils.enum.aws_enum import AwsServiceEnum
from core.domains.board.repository.board_repository import BoardRepository


class S3Helper:
    @inject.autoparams
    def __init__(self, board_repo: BoardRepository):
        self._board_repo = board_repo

    def upload(self, bucket, path, file, extension):
        """
        :param bucket: s3 bucket
        :param path: 저장할 경로
        :param file: 파일
        :param extension: 파일 확장자
        :return:
        """
        client = boto3.client(
            AwsServiceEnum.S3.value,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        object_name = path + uuid + "." + extension
        try:
            client.upload_file(file, bucket, object_name)
        except ClientError as e:
            # TODO: log
            return False
        return True
