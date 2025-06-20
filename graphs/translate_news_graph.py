from agents.rss_reader_agent import RSSReaderAgent
from agents.diff_detector_agent import DiffDetectorAgent
from agents.translator_agent import TranslatorAgent
from schemas.rss_schema import Article
from schemas.diff_schema import DiffResult
from schemas.translation_schema import TranslationResult

# RSSフィードURL（例）
jp_feeds = ["https://news.yahoo.co.jp/rss/topics/top-picks.xml"]
intl_feeds = ["https://rss.nytimes.com/services/xml/rss/nyt/World.xml"]

# Step 1: RSS取得
jp_articles: list[Article] = RSSReaderAgent(jp_feeds).run()
intl_articles: list[Article] = RSSReaderAgent(intl_feeds).run()

# Step 2: 差分検出
diff_articles: list[DiffResult] = DiffDetectorAgent(jp_articles, intl_articles).run()

# Step 3: 翻訳処理
translated_results: list[TranslationResult] = TranslatorAgent().run(diff_articles)

# 出力確認（デモ用）
for result in translated_results:
    print("🌍", result.original.title)
    print("🈁", result.translated_text)
    print()
