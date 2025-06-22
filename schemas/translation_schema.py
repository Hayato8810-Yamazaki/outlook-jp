from pydantic import BaseModel
from schemas.rss_schema import Article

class TranslationResult(BaseModel):
    original: Article
    translated_title: str
    language: str = "ja"
