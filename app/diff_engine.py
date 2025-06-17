import requests
import os

from difflib import SequenceMatcher

# 日本の主要ニュースを取得（簡易版、必要に応じてニュースAPIを拡張）
def fetch_japan_news(topic):
    # 例：NewsAPI で日本語ニュース取得
    api_key = os.getenv("NEWSAPI_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={topic}&language=ja&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "articles" not in data or len(data["articles"]) == 0:
        return []

    return [article["title"] for article in data["articles"] if article.get("title")]

# 海外ニュースと日本のニュースを比較
def compare_with_japan_news(foreign_article_title: str, topic: str = "") -> bool:
    """
    比較して「日本で報道されていない」と判断されたら True を返す
    """
    japan_titles = fetch_japan_news(topic)

    for jp_title in japan_titles:
        similarity = SequenceMatcher(None, foreign_article_title, jp_title).ratio()
        if similarity > 0.6:  # 類似度が高ければ既報とみなす（しきい値は調整可）
            return True  # 報道されている

    return False  # 報道されていない
