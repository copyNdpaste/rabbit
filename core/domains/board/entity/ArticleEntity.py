from dataclasses import dataclass
from datetime import datetime


@dataclass
class ArticleEntity:
    id: int
    post_id: int
    body: str
    created_at: datetime
    updated_at: datetime
