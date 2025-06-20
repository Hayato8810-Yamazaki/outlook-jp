from typing import List
from agents.base_agent import BaseAgent
from schemas.rss_schema import Article
from schemas.diff_schema import DiffResult
from tools.similarity import calculate_similarity

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
                        description=intl_article.description,
                        link=intl_article.link
                    )
                )
        return diff_articles

    def _has_similar(self, intl_article: Article) -> bool:
        for jp_article in self.jp_articles:
            similarity = calculate_similarity(intl_article.title, jp_article.title)
            if similarity > 0.3:
                return True
        return False
