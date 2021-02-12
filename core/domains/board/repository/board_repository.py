from typing import List, Optional, Union

from app.extensions.database import session
from app.persistence.model.article_model import ArticleModel
from app.persistence.model.post_like_count_model import PostLikeCountModel
from app.persistence.model.post_like_state_model import PostLikeStateModel
from app.persistence.model.post_model import PostModel
from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.entity.like_entity import (
    PostLikeStateEntity,
    PostLikeCountEntity,
)
from core.domains.board.entity.post_entity import PostEntity
from core.domains.board.enum.post_enum import PostLimitEnum, PostLikeStateEnum


class BoardRepository:
    def create_post(self, dto: CreatePostDto) -> Optional[PostEntity]:
        try:
            post = PostModel(
                user_id=dto.user_id,
                title=dto.title,
                region_group_id=dto.region_group_id,
                type=dto.type,
                is_comment_disabled=dto.is_comment_disabled,
                is_deleted=dto.is_deleted,
                is_blocked=dto.is_blocked,
                report_count=dto.report_count,
                read_count=dto.read_count,
                category=dto.category,
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

            return post.to_entity()
        except Exception as e:
            # TODO : log e 필요
            session.rollback()
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
                        "category": dto.category,
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
            # TODO : log
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
            return None

    def is_post_exist(self, post_id: int) -> bool:
        return session.query(
            session.query(PostModel).filter_by(id=post_id).exists()
        ).scalar()

    def get_post_list(
        self,
        region_group_id: int,
        previous_post_id: int = None,
        title: str = "",
        category: int = 0,
    ) -> Optional[List[Union[PostEntity, list]]]:
        """
        :param region_group_id: 유저가 속한 동네 식별자
        :param previous_post_id: 유저가 바로 직전 조회한 post id
        :param title: 게시글 제목
        :param category: 상품 카테고리
        :return: post list
        1. 동일 지역의 post 가져오기, deleted, blocked 제외
        2. title like 검색, 선택된 type, category 등에 맞게 응답
        """
        category_filter = []
        if category:
            category_filter.append(PostModel.category == category)
        search_filter = []
        if title:
            search_filter.append(PostModel.title.like(f"%{title}%"))
        previous_post_id_filter = []
        if previous_post_id:
            previous_post_id_filter.append(PostModel.id > previous_post_id)
        try:
            post_list = (
                session.query(PostModel)
                .filter(
                    PostModel.region_group_id == region_group_id,
                    PostModel.is_blocked == False,
                    PostModel.is_deleted == False,
                    *category_filter,
                    *search_filter,
                    *previous_post_id_filter,
                )
                .order_by(PostModel.id.desc())
                .limit(PostLimitEnum.LIMIT.value)
                .all()
            )

            return [post.to_post_list_entity() for post in post_list]
        except Exception as e:
            # TODO : log 추가
            pass

    def get_post(self, post_id: int) -> Optional[PostEntity]:
        post = session.query(PostModel).filter_by(id=post_id).first()

        return post.to_entity() if post else None

    def add_read_count(self, post_id: int) -> bool:
        try:
            session.query(PostModel).filter_by(id=post_id).update(
                {"read_count": PostModel.read_count + 1}
            )
            return True
        except Exception as e:
            # TODO : log
            session.rollback()
            return False

    def create_post_like_count(self, post_id) -> Optional[PostLikeCountEntity]:
        try:
            post_like_count = PostLikeCountModel(post_id=post_id)

            session.add(post_like_count)
            session.commit()
            return post_like_count.to_entity()
        except Exception as e:
            # TODO : log
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
            # TODO : log
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
            # TODO : log
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
            # TODO : log
            session.rollback()
            return None
