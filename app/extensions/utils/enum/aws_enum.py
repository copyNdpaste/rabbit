from enum import Enum


class AwsServiceEnum(Enum):
    S3 = "s3"


class S3BucketEnum(Enum):
    LUDICER_BUCKET = "ludicer_bucket"


class S3PathEnum(Enum):
    PROFILE_IMGS = "profile_imgs/"
    POST_IMGS = "post_imgs/"
