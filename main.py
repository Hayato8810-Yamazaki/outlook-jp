from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.model_router import router as model_router

# 環境変数の読み込み
load_dotenv()

# FastAPI アプリケーションの作成
app = FastAPI()

# ルーターの登録
app.include_router(model_router)

# デフォルトルート（オプション）
@app.get("/")
def read_root():
    return {"message": "Hello from Outlook JP!"}
