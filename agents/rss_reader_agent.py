from typing import List, Dict, Any
import feedparser
from agents.base_agent import BaseAgent  # BaseAgent を自前で定義

class RSSReaderAgent(BaseAgent):
    def __init__(self, feed_urls: List[str]):
        self.feed_urls = feed_urls

    def run(self, input_data: Any = None) -> List[Dict[str, str]]:
        """
        RSS フィードを読み取り、記事タイトルとリンクを返す
        """
        articles = []
        for url in self.feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                articles.append({
                    "title": entry.title,
                    "link": entry.link
                })
        return articles
