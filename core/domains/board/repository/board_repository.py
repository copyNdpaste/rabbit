from typing import List, Optional, Union
from app.extensions.database import session
from app.extensions.utils.log_helper import logger_
from app.persistence.model.article_model import ArticleModel
from app.persistence.model.attachment_model import AttachmentModel
from app.persistence.model.category_model import CategoryModel
from app.persistence.model.post_category_model import PostCategoryModel
from app.persistence.model.post_like_count_model import PostLikeCountModel
from app.persistence.model.post_like_state_model import PostLikeStateModel
from app.persistence.model.post_model import PostModel
from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.entity.attachment_entiry import AttachmentEntity
from core.domains.board.entity.like_entity import (
    PostLikeStateEntity,
    PostLikeCountEntity,
)
from core.domains.board.entity.post_entity import PostEntity
from core.domains.board.enum.post_enum import (
    PostLimitEnum,
    PostLikeStateEnum,
    PostStatusEnum,
)

logger = logger_.getLogger(__name__)


class BoardRepository:
    def create_post(self, dto: CreatePostDto) -> Optional[PostEntity]:
        try:
            post = PostModel(
                user_id=dto.user_id,
                title=dto.title,
                region_group_id=dto.region_group_id,
                type=dto.type,
                is_comment_disabled=dto.is_comment_disabled,
                amount=dto.amount,
                unit=dto.unit,
                price_per_unit=dto.price_per_unit,
                status=dto.status,
            )
            session.add(post)
            session.commit()

            article = ArticleModel(post_id=post.id, body=dto.body)
            session.add(article)
            session.commit()

            self.create_post_categories(post_id=post.id, dto=dto)

            return post.to_entity()
        except Exception as e:
            logger.error(
                f"[BoardRepository][create_post] user_id : {dto.user_id} title : {dto.title} "
                f"region_group_id : {dto.region_group_id} type : {dto.type} "
                f"is_comment_disabled : {dto.is_comment_disabled} amount : {dto.amount} unit : {dto.unit} "
                f"price_per_unit : {dto.price_per_unit} status : {dto.status} error : {e}"
            )
            session.rollback()
            return None

    def create_post_categories(self, post_id: int, dto: CreatePostDto):
        post_categories = []

        try:
            for category_id in dto.category_ids:
                post_categories.append(
                    PostCategoryModel(post_id=post_id, category_id=category_id)
                )

            session.add_all(post_categories)
            session.commit()
        except Exception as e:
            logger.error(
                f"[BoardRepository][create_post_categories] post_id : {post_id} error : {e}"
            )
            session.rollback()
            return False

    def create_attachment(
        self,
        post_id: int,
        type: str,
        file_name: str,
        path: str,
        extension: str,
        uuid: str,
    ) -> Optional[AttachmentEntity]:
        try:
            attachment = AttachmentModel(
                post_id=post_id,
                type=type,
                file_name=file_name,
                path=path,
                extension=extension,
                uuid=uuid,
            )
            session.add(attachment)
            session.commit()
            return attachment.to_entity() if attachment else None
        except Exception as e:
            session.rollback()
            logger.error(
                f"[BoardRepository][create_attachment] post_id : {post_id} type : {type} file_name : {file_name} "
                f"path : {path} extension : {extension} uuid : {uuid} error : {e}"
            )
            return None

    def _get_post(self, post_id) -> PostEntity:
        return session.query(PostModel).filter_by(id=post_id).first().to_entity()

    def update_post(self, dto: UpdatePostDto) -> Optional[PostEntity]:
        try:
            (
                session.query(PostModel)
                .filter(PostModel.id == dto.post_id)
                .update(
                    {
                        "title": dto.title,
                        "region_group_id": dto.region_group_id,
                        "type": dto.type,
                        "is_comment_disabled": dto.is_comment_disabled,
                    }
                )
            )
            session.query(ArticleModel).filter_by(post_id=dto.post_id).update(
                {"body": dto.body}
            )
            post_entity = self._get_post(post_id=dto.post_id)
            return post_entity if post_entity else None
        except Exception as e:
            session.rollback()
            logger.error(
                f"[BoardRepository][update_post] title : {dto.title} region_group_id : {dto.region_group_id} "
                f"type : {dto.type} is_comment_disabled : {dto.is_comment_disabled} error : {e}"
            )
            return None

    def is_post_owner(self, dto) -> bool:
        post = self._get_post(post_id=dto.post_id)
        return True if post.user_id == dto.user_id else False

    def delete_post(self, dto: DeletePostDto) -> Optional[PostEntity]:
        try:
            session.query(PostModel).filter_by(id=dto.post_id).update(
                {"is_deleted": True}
            )
            return self._get_post(post_id=dto.post_id)
        except Exception as e:
            session.rollback()
            logger.error(
                f"[BoardRepository][delete_post] post_id : {dto.post_id} error : {e}"
            )
            return None

    def is_post_exist(self, post_id: int) -> bool:
        return session.query(
            session.query(PostModel).filter_by(id=post_id).exists()
        ).scalar()

    # TODO: parameter ?????? ???????????? dto ?????? ??????, type??? ?????? ??????...
    def get_post_list(
        self,
        region_group_id: int,
        previous_post_id: int = None,
        title: str = "",
        category_ids: list = None,
        status: str = None,
    ) -> Optional[List[Union[PostEntity, list]]]:
        """
        :param category_ids: ?????? ????????????
        :param status: post ?????? ??????
        :param region_group_id: ????????? ?????? ?????? ?????????
        :param previous_post_id: ????????? ?????? ?????? ????????? post id
        :param title: ????????? ??????
        :return: post list
        1. ?????? ????????? post ????????????, deleted, blocked ??????
        2. title like ??????, ????????? type, category ?????? ?????? ??????
        """

        if not category_ids:
            category_ids = self.get_category_ids()

        search_filter = []
        if title:
            search_filter.append(PostModel.title.like(f"%{title}%"))

        previous_post_id_filter = []
        if previous_post_id:
            previous_post_id_filter.append(PostModel.id < previous_post_id)

        status_filters = []
        if status == PostStatusEnum.EXCLUDE_COMPLETED.value:  # ?????? ?????? ??? ?????????
            status_filters.append(PostModel.status == PostStatusEnum.SELLING.value)
        elif status == PostStatusEnum.ALL.value:  # ?????????, ?????? ?????? ??? ??????
            status_filters.append([PostModel.status == PostStatusEnum.SELLING.value])
            status_filters.append([PostModel.status == PostStatusEnum.COMPLETED.value])

        try:
            # TODO:?????? ???????????? ???????????? ??????
            # status??? ?????? ????????? or ????????? + ?????? ?????? ??????
            if len(status_filters) >= 2:
                query_list = []
                for status_filter in status_filters:
                    query_list.append(
                        session.query(PostModel).filter(
                            PostModel.region_group_id == region_group_id,
                            PostModel.is_blocked == False,
                            PostModel.is_deleted == False,
                            *search_filter,
                            *previous_post_id_filter,
                            *status_filter,
                        )
                    )
                query = query_list[0].union(*query_list[1:])
            else:
                query = session.query(PostModel).filter(
                    PostModel.region_group_id == region_group_id,
                    PostModel.is_blocked == False,
                    PostModel.is_deleted == False,
                    *search_filter,
                    *previous_post_id_filter,
                    *status_filters,
                )

            query_list = []
            for category_id in category_ids:
                q = query
                query_list.append(
                    q.filter(
                        PostModel.id == PostCategoryModel.post_id,
                        PostCategoryModel.category_id == CategoryModel.id,
                        CategoryModel.id == category_id,
                    )
                )

            post_list = []
            if query_list:
                query = query_list[0].union(*query_list[1:])

                post_list = (
                    query.order_by(PostModel.id.desc())
                    .limit(PostLimitEnum.LIMIT.value)
                    .all()
                )

            return [post.to_post_list_entity() for post in post_list]
        except Exception as e:
            logger.error(f"[BoardRepository][get_post_list] error : {e}")
            return []

    def get_post(
        self, post_id: int, is_deleted: bool = False, is_blocked: bool = False
    ) -> Optional[PostEntity]:
        post = (
            session.query(PostModel)
            .filter_by(id=post_id, is_deleted=is_deleted, is_blocked=is_blocked)
            .first()
        )

        return post.to_entity() if post else None

    def add_read_count(self, post_id: int) -> bool:
        try:
            session.query(PostModel).filter_by(id=post_id).update(
                {"read_count": PostModel.read_count + 1}
            )
            return True
        except Exception as e:
            logger.error(
                f"[BoardRepository][add_read_count] post_id : {post_id} error : {e}"
            )
            session.rollback()
            return False

    def create_post_like_count(self, post_id) -> Optional[PostLikeCountEntity]:
        try:
            post_like_count = PostLikeCountModel(post_id=post_id)

            session.add(post_like_count)
            session.commit()
            return post_like_count.to_entity()
        except Exception as e:
            logger.error(
                f"[BoardRepository][create_post_like_count] post_id : {post_id} error : {e}"
            )
            session.rollback()
            return None

    def get_post_like_count(self, post_id: int) -> Optional[PostLikeCountEntity]:
        post_like_count = (
            session.query(PostLikeCountModel).filter_by(post_id=post_id).first()
        )

        return post_like_count.to_entity() if post_like_count else None

    def update_post_like_count(self, post_id: int, count: int) -> bool:
        try:
            session.query(PostLikeCountModel).filter_by(post_id=post_id).update(
                {"count": PostLikeCountModel.count + count}
            )
            return True
        except Exception as e:
            logger.error(
                f"[BoardRepository][update_post_like_count] post_id : {post_id} count : {count} error : {e}"
            )
            session.rollback()
            return False

    def get_post_like_state(
        self, user_id: int, post_id: int
    ) -> Optional[PostLikeStateEntity]:
        post_like_state = (
            session.query(PostLikeStateModel)
            .filter_by(user_id=user_id, post_id=post_id)
            .first()
        )

        return post_like_state.to_entity() if post_like_state else None

    def create_post_like_state(self, user_id: int, post_id: int):
        try:
            post_like_state = PostLikeStateModel(
                user_id=user_id, post_id=post_id, state=PostLikeStateEnum.LIKE.value
            )
            session.add(post_like_state)
            session.commit()

            return self.get_post_like_state(user_id=user_id, post_id=post_id)
        except Exception as e:
            logger.error(
                f"[BoardRepository][create_post_like_state] post_id : {post_id} user_id : {user_id} error : {e}"
            )
            session.rollback()
            return False

    def update_post_like_state(
        self, user_id: int, post_id: int, state: str
    ) -> Optional[PostLikeStateEntity]:
        try:
            session.query(PostLikeStateModel).filter_by(
                user_id=user_id, post_id=post_id,
            ).update({"state": state})

            return self.get_post_like_state(user_id=user_id, post_id=post_id)
        except Exception as e:
            logger.error(
                f"[BoardRepository][create_post_like_state] post_id : {post_id} user_id : {user_id} state : {state}"
                f" error : {e}"
            )
            session.rollback()
            return None

    def get_category_ids(self) -> list:
        category_ids = (
            session.query(CategoryModel).with_entities(CategoryModel.id).all()
        )

        return [category_id[0] for category_id in category_ids]

    def get_selling_post_list(self, user_id: int, previous_post_id: int = None) -> list:
        previous_post_id_filter = []
        if previous_post_id:
            previous_post_id_filter.append(PostModel.id < previous_post_id)

        post_list = (
            session.query(PostModel)
            .filter(PostModel.user_id == user_id, *previous_post_id_filter)
            .order_by(PostModel.id.desc())
            .limit(PostLimitEnum.LIMIT.value)
            .all()
        )

        return [post.to_entity() for post in post_list]

    def get_like_post_list(self, user_id: int, previous_post_id: int = None) -> list:
        previous_post_id_filter = []
        if previous_post_id:
            previous_post_id_filter.append(PostModel.id < previous_post_id)

        post_list = (
            session.query(PostModel)
            .join(PostLikeStateModel)
            .filter(*previous_post_id_filter, PostLikeStateModel.user_id == user_id)
            .order_by(PostModel.id.desc())
            .limit(PostLimitEnum.LIMIT.value)
            .all()
        )

        return [post.to_entity() for post in post_list]

    def get_attachments(self, post_id: int) -> list:
        attachments = session.query(AttachmentModel).filter_by(post_id=post_id).all()

        return [attachment.to_entity() for attachment in attachments]

    def delete_attachments(self, post_id: int) -> bool:
        try:
            session.query(AttachmentModel).filter_by(post_id=post_id).delete()
            return True
        except Exception as e:
            logger.error(
                f"[BoardRepository][delete_attachments] post_id : {post_id} error : {e}"
            )
            session.rollback()
            return False

    def add_report_count(self, post_id: int) -> Union[int, bool]:
        try:
            session.query(PostModel).filter_by(id=post_id).update(
                {"report_count": PostModel.report_count + 1}
            )
            return self._get_post(post_id=post_id).report_count
        except Exception as e:
            logger.error(
                f"[BoardRepository][add_report_count] post_id : {post_id} error : {e}"
            )
            session.rollback()
            return False

    def block(self, post_id: int) -> bool:
        try:
            session.query(PostModel).filter_by(id=post_id).update({"is_blocked": True})
            return True
        except Exception as e:
            logger.error(f"[BoardRepository][block] post_id : {post_id} error : {e}")
            session.rollback()
            return False
