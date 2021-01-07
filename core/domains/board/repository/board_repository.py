from typing import List, Optional

from app.extensions.database import session
from app.persistence.model.post_model import PostModel
from core.domains.board.dto.post_dto import CreatePostDto, UpdatePostContentDto
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
            return post.to_entity()
        except Exception as e:
            # TODO : log e 필요
            session.rollback()
            return None

    def get_posts(self, user_id: int) -> List[PostEntity]:
        posts = session.query(PostModel).filter_by(user_id=user_id).all()

        return [board.to_entity() for board in posts]

    def get_post(self, id) -> PostEntity:
        return session.query(PostModel).filter_by(id=id).first()

    def update_post(self, dto: UpdatePostContentDto) -> Optional[PostEntity]:
        try:
            (
                session.query(PostModel)
                .filter_by(id=dto.id)
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
            return self.get_post(id=dto.id)
        except Exception as e:
            session.rollback()
            # TODO : log
            return None
