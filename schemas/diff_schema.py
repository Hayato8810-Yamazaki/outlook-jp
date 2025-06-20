from pydantic import BaseModel
from typing import List
from schemas.rss_schema import Article

class DiffResult(BaseModel):
    missing_in_japan: List[Article]
