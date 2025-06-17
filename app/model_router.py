from fastapi import APIRouter, Query
from app.translator import translate_to_japanese

router = APIRouter()

@router.get("/translate_news")
async def translate_news(topic: str = Query(...)):
    try:
        english_news = f"The latest update on {topic} shows significant international reactions."
        translated = translate_to_japanese(english_news)
        return {
            "original": english_news,
            "translated": translated
        }
    except Exception as e:
        return {"error": str(e)}
