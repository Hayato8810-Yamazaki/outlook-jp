import feedparser
import os
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数の読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# キーワード
keywords = ["Japan", "Tokyo", "Yen", "Fukushima", "Prime Minister", "Nuclear", "Toshiba", "Olympics", "Nissan", "Scandal", "Corruption"]

# RSSフィード定義
foreign_rss_urls = {
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition_world.rss",
    "Reuters": "https://feeds.reuters.com/reuters/worldNews"
}

japan_rss_urls = {
    "NHK": "https://www3.nhk.or.jp/rss/news/cat0.xml",
    "Yahoo": "https://news.yahoo.co.jp/rss/topics/top-picks.xml",
    "Mainichi": "https://mainichi.jp/rss/etc/mainichi-flash.rss",
    "Asahi": "https://www.asahi.com/rss/asahi/newsheadlines.rdf"
}

# RSSからキーワード一致する見出しを抽出
def fetch_headlines(urls, keywords):
    def fetch_headlines(urls, keywords):
    headlines = set()
    for source, url in urls.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "")
            description = entry.get("description", "")
            combined = f"{title} {description}"
            if any(kw.lower() in combined.lower() for kw in keywords):
                headlines.add(combined.strip())
    return headlines

# ニュース取得
foreign = fetch_headlines(foreign_rss_urls, keywords)
japanese = fetch_headlines(japan_rss_urls, keywords)

# 差分抽出
diff = foreign - japanese
diff_list = list(diff)

# 翻訳処理
def translate_to_japanese(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはプロの翻訳家です。英語のニュース見出しを自然な日本語に訳してください。"},
            {"role": "user", "content": f"Translate this to Japanese:\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

# 出力
print("\n🌍 海外で報道されているが日本では報道されていない可能性のある話題：\n")
for i, headline in enumerate(diff_list[:5], 1):  # 上位5件だけ表示
    translated = translate_to_japanese(headline)
    print(f"{i}. {headline}")
    print(f"   🈁 翻訳: {translated}\n")
