from typing import List
from agents.base_agent import BaseAgent
from schemas.rss_schema import Article

class JapanFilterAgent(BaseAgent):
    """Filter articles to those that mention Japan-related keywords."""

    def __init__(self, keywords: List[str] | None = None):
        default_keywords = [
            "japan",
            "tokyo",
            "fukushima",
            "osaka",
            "okinawa",
            "yen",
            "kishida",
            "ldp",
            "japanese",
            "olympics",
            "nissan",
            "toyota",
            "toshiba",
            "shinkansen",
        ]
        self.keywords = [k.lower() for k in (keywords or default_keywords)]

    def run(self, articles: List[Article]) -> List[Article]:
        filtered: List[Article] = []
        for article in articles:
            text = f"{article.title} {article.description or ''}".lower()
            if any(kw in text for kw in self.keywords):
                filtered.append(article)
        return filtered
