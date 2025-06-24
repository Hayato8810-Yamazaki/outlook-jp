from agents.rss_reader_agent import RSSReaderAgent
from agents.diff_detector_agent import DiffDetectorAgent
from schemas.rss_schema import Article  # ← 追加！

intl_urls = ["https://rss.nytimes.com/services/xml/rss/nyt/World.xml"]
jp_urls = ["https://news.yahoo.co.jp/rss/topics/top-picks.xml"]

# RSS 記事の取得
intl_articles_raw = RSSReaderAgent(intl_urls).run()
jp_articles_raw = RSSReaderAgent(jp_urls).run()

# dict → Article 型に変換
intl_articles = [Article(**a) if isinstance(a, dict) else a for a in intl_articles_raw]
jp_articles = [Article(**a) if isinstance(a, dict) else a for a in jp_articles_raw]

# 差分検出
agent = DiffDetectorAgent(jp_articles, intl_articles)
diffs = agent.run()

# 表示
print(f"\n🆕 日本で報道されていない可能性のある海外ニュース: {len(diffs)} 件\n")
for idx, article in enumerate(diffs[:5], 1):
    print(f"{idx}. {article.title}\n   {article.link}")
