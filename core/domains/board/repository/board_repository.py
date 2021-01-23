from typing import List, Optional

from app.extensions.database import session
from app.persistence.model.article_model import ArticleModel
from app.persistence.model.post_model import PostModel
from app.persistence.model.user_model import UserModel
from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostDto, DeletePostDto
from core.domains.board.entity.post_entity import PostEntity


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

    def get_posts(self, user_id: int) -> List[PostEntity]:
        posts = session.query(PostModel).filter_by(user_id=user_id).all()

        return [post.to_entity() for post in posts]

    def get_post(self, id) -> PostEntity:
        return session.query(PostModel).filter_by(id=id).first().to_entity()

    def update_post(self, dto: UpdatePostDto) -> Optional[PostEntity]:
        try:
            (
                session.query(PostModel)
                .filter(PostModel.id == dto.id)
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
            session.query(ArticleModel).filter_by(post_id=dto.id).update(
                {"body": dto.body}
            )
            return self.get_post(id=dto.id)
        except Exception as e:
            session.rollback()
            # TODO : log
            return None

    def is_post_owner(self, dto) -> bool:
        post = self.get_post(id=dto.id)
        return True if post.user_id == dto.user_id else False

    def delete_post(self, dto: DeletePostDto) -> Optional[PostEntity]:
        try:
            session.query(PostModel).filter_by(id=dto.id).update({"is_deleted": True})
            return self.get_post(id=dto.id)
        except Exception as e:
            session.rollback()
            return None

    def is_post_exist(self, post_id: int) -> bool:
        return session.query(
            session.query(PostModel).filter_by(id=post_id).exists()
        ).scalar()

    def get_post_list(self, region_group_id: int) -> Optional[List[PostEntity]]:
        """ TODO
        1. 동일 지역의 post 가져오기, 삭제된 거 제외, block 제외
        2. 검색 filter 넣기, keyword like 검색, 선택된 type, category 등에 맞게 응답
        3. 응답 값 created_at, title, user 정보, type, read_count, hashtag
        region_group에 속한 region 목록..
        """
        try:
            post_list = (
                session.query(PostModel)
                .outerjoin("article")
                .join(PostModel.user)
                .join(UserModel.region)
                .join(UserModel.user_profile)
                .filter(
                    PostModel.region_group_id == region_group_id,
                    PostModel.is_blocked == False,
                    PostModel.is_deleted == False,
                )
                .order_by(PostModel.id.desc())
                .limit(10)
                .all()
            )

            return [post.to_post_list_entity() for post in post_list]
        except Exception as e:
            pass

    def get_post(self) -> PostEntity:
        """
        TODO
        1. 삭제, 블락 정보, 유저 정보, 제목, article body, type, 댓글 사용 가능 여부, 조회 수, 카테고리,
        """
        pass
