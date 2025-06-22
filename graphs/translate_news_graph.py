from agents.rss_reader_agent import RSSReaderAgent
from agents.diff_detector_agent import DiffDetectorAgent
from agents.translator_agent import TranslatorAgent
from schemas.rss_schema import Article
from schemas.diff_schema import DiffResult
from schemas.translation_schema import TranslationResult
from typing import List


class AgentGraph:
    def __init__(self, intl_feeds: List[str], jp_feeds: List[str]):
        self.intl_feeds = intl_feeds
        self.jp_feeds = jp_feeds

    def run(self) -> List[TranslationResult]:
        # ステップ 1: 海外と日本のニュースを収集
        intl_articles: List[Article] = RSSReaderAgent(self.intl_feeds).run()
        jp_articles: List[Article] = RSSReaderAgent(self.jp_feeds).run()

        # ステップ 2: 差分検出
        diff_articles: List[Article] = DiffDetectorAgent(jp_articles, intl_articles).run()

        # ステップ 3: 翻訳
        translations: List[TranslationResult] = []
        for article in diff_articles:
            result = TranslatorAgent().run(article)
            translations.append(result)

        return translations


if __name__ == "__main__":
    # CLI風呼び出し例
    intl = ["https://rss.nytimes.com/services/xml/rss/nyt/World.xml"]
    jp = ["https://news.yahoo.co.jp/rss/topics/top-picks.xml"]

    graph = AgentGraph(intl_feeds=intl, jp_feeds=jp)
    results = graph.run()

    print("\n\U0001F30D 海外で報道されているが日本では報道されていない可能性のある話題：")
    for idx, r in enumerate(results, 1):
        print(f"\n{idx}. {r.original.title}\n   \U0001F238 翻訳: {r.translated_title}")
