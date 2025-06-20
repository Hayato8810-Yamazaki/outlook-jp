from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    title: str
    description: Optional[str] = None
    link: Optional[str] = None
    published: Optional[str] = None

class RSSFeed(BaseModel):
    source: str  # 例: "NYTimes World"
    articles: list[Article]
