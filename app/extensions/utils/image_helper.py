import boto3
from botocore.exceptions import ClientError
from flask import current_app

from app.extensions.utils.enum.aws_enum import AwsServiceEnum


class S3Helper:
    @classmethod
    def upload(cls, bucket, file_name, object_name):
        """
        :param bucket: s3 bucket
        :param path: 저장할 경로
        :param file_and_extension: 파일
        :return:
        """
        client = boto3.client(
            AwsServiceEnum.S3.value,
            aws_access_key_id=current_app.config.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=current_app.config.get("AWS_SECRET_ACCESS_KEY"),
        )

        try:
            client.upload_file(
                Filename=file_name, Bucket=bucket, Key=object_name,
            )
        except ClientError as e:
            # TODO: log
            return False
        return True
