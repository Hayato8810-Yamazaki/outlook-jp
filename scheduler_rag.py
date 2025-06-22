import schedule
import time
from datetime import datetime

from agents.translate_news_graph import AgentGraph
from schemas.translation_schema import TranslationResult
from tools.chroma_store import save_translation, find_similar  # ChromaDB 関連

# === 設定 ===
intl_feeds = ["https://rss.nytimes.com/services/xml/rss/nyt/World.xml"]
jp_feeds = ["https://news.yahoo.co.jp/rss/topics/top-picks.xml"]

# === ChromaDB: 類似翻訳が既にあるか確認 ===
def is_new_article_chroma(new_result: TranslationResult) -> bool:
    similar = find_similar(new_result.original.title)
    return similar['documents'] == []  # 類似がなければ新規

# === メイン処理 ===
def job():
    print(f"[INFO] 実行時刻: {datetime.now()}")
    graph = AgentGraph(intl_feeds=intl_feeds, jp_feeds=jp_feeds)
    results = graph.run()

    new_items = []

    for r in results:
        if is_new_article_chroma(r):
            print("\n🆕 新しい翻訳:")
            print(f"{r.original.title}\n🈁 翻訳: {r.translated_title}")
            save_translation(r)
            new_items.append(r)

    if new_items:
        print(f"[INFO] {len(new_items)} 件を ChromaDB に保存しました。")
    else:
        print("[INFO] 新しいニュースはありませんでした。")

# === 定期実行スケジュール設定（例：12時間ごと） ===
schedule.every(720).minutes.do(job)

if __name__ == "__main__":
    print("スケジューラを開始します... Ctrl+C で停止")
    job()  # 初回実行
    while True:
        schedule.run_pending()
        time.sleep(10)
