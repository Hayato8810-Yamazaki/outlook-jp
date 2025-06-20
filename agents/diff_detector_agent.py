from typing import Any, List, Dict
from agents.base_agent import BaseAgent
from tools.similarity import calculate_similarity

class DiffDetectorAgent(BaseAgent):
    def __init__(self, jp_articles: List[Dict], intl_articles: List[Dict]):
        """
        :param jp_articles: 日本のRSS記事のリスト（例：{'title': '...', 'description': '...'}）
        :param intl_articles: 海外のRSS記事のリスト
        """
        self.jp_articles = jp_articles
        self.intl_articles = intl_articles

    def run(self, input_data: Any = None) -> List[Dict]:
        """
        日本には存在しない（類似記事がない）海外ニュースを検出して返す
        """
        diff_articles = []

        for intl_article in self.intl_articles:
            intl_text = f"{intl_article.get('title', '')} {intl_article.get('description', '')}"
            if not self._is_similar_to_any_jp(intl_text):
                diff_articles.append(intl_article)

        return diff_articles

    def _is_similar_to_any_jp(self, intl_text: str, threshold: float = 0.3) -> bool:
        """
        類似度で日本記事と比較し、閾値以上なら「類似している」とみなす
        """
        for jp_article in self.jp_articles:
            jp_text = f"{jp_article.get('title', '')} {jp_article.get('description', '')}"
            similarity = calculate_similarity(intl_text, jp_text)
            if similarity >= threshold:
                return True
        return False
