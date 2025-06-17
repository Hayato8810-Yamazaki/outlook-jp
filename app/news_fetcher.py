import os
import requests
from dotenv import load_dotenv

load_dotenv()  # .envファイルを読み込む場合はこれを有効にする

def fetch_news(topic):
    api_key = os.getenv("NEWSAPI_API_KEY")
    if not api_key:
        raise ValueError("NEWSAPI_API_KEYが設定されていません")
    
    url = f"https://newsapi.org/v2/everything?q={topic}&language=en&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "articles" not in data or not data["articles"]:
        return "記事が見つかりませんでした"

    article = data["articles"][0]
    return f"{article['title']} — {article['description']}"
