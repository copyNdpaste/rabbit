import os
import uuid
import inject
from typing import Union
from app.extensions.utils.enum.aws_enum import S3PathEnum, S3BucketEnum
from app.extensions.utils.image_helper import S3Helper
from core.domains.user.dto.user_dto import GetUserDto, UpdateUserDto
from core.domains.user.repository.user_repository import UserRepository
from core.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput, FailureType


class GetUserUseCase:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def execute(
        self, dto: GetUserDto
    ) -> Union[UseCaseSuccessOutput, UseCaseFailureOutput]:
        user = self._user_repo.get_user(user_id=dto.user_id)
        if not user:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)
        return UseCaseSuccessOutput(value=user)


class UpdateUserUseCase:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def execute(
        self, dto: UpdateUserDto
    ) -> Union[UseCaseSuccessOutput, UseCaseFailureOutput]:
        user = self._user_repo.get_user(user_id=dto.user_id)
        if not user:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        user = self._user_repo.update_user(
            user_id=dto.user_id,
            nickname=dto.nickname,
            status=dto.status,
            region_id=dto.region_id,
        )
        if not user:
            return UseCaseFailureOutput(type=FailureType.SYSTEM_ERROR)

        attachment = self._upload_picture(dto=dto, user_profile_id=user.profile_id)
        if not attachment:
            return UseCaseFailureOutput(FailureType.SYSTEM_ERROR)

        user.user_profile = (
            attachment[0].path + attachment[0].uuid + attachment[0].extension
            if attachment[0]
            else ""
        )

        return UseCaseSuccessOutput(value=user)

    def _upload_picture(self, dto, user_profile_id: int):
        attachment_list = []

        for file in dto.files:
            f, extension = os.path.splitext(file.filename)
            uuid_ = str(uuid.uuid4())
            object_name = S3PathEnum.POST_IMGS.value + uuid_ + extension

            res = S3Helper.upload(
                bucket=S3BucketEnum.LUDICER_BUCKET.value,
                file_name=file,
                object_name=object_name,
            )

            if not res:
                return False

            attachment = self._user_repo.update_user_profile(
                user_profile_id=user_profile_id,
                file_name=f,
                path=S3PathEnum.POST_IMGS.value,
                extension=extension,
                uuid=uuid_,
            )
            if not attachment:
                return False
            attachment_list.append(attachment)

        return attachment_list
