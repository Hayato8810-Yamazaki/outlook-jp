from typing import List
from agents.base_agent import BaseAgent
from schemas.rss_schema import Article
from schemas.diff_schema import DiffResult
from tools.embedding_utils import translate_to_english, get_embedding, cosine_similarity

class DiffDetectorAgent(BaseAgent):
    def __init__(self, jp_articles: List[Article], intl_articles: List[Article]):
        self.jp_articles = jp_articles
        self.intl_articles = intl_articles

    def run(self, input_data=None) -> List[DiffResult]:
        diff_articles = []
        for intl_article in self.intl_articles:
            if not self._has_similar(intl_article):
                diff_articles.append(
                    DiffResult(
                        title=intl_article.title,
                        description=intl_article.description if intl_article.description is not None else None,
                        link=intl_article.link,
                        missing_in_japan=True
                    )
                )
        return diff_articles

    def _has_similar(self, intl_article: Article) -> bool:
        # タイトル + 説明を比較対象に
        intl_text = f"{intl_article.title} {intl_article.description or ''}"
        intl_text_en = translate_to_english(intl_text)
        intl_emb = get_embedding(intl_text_en)

        for jp_article in self.jp_articles:
            jp_text = f"{jp_article.title} {jp_article.description or ''}"
            jp_text_en = translate_to_english(jp_text)
            jp_emb = get_embedding(jp_text_en)

            similarity = cosine_similarity(intl_emb, jp_emb)
            if similarity > 0.7:  # 類似と見なす閾値
                return True

        return False
