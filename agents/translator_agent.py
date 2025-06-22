import os
from openai import OpenAI
from agents.base_agent import BaseAgent
from schemas.translation_schema import TranslationResult
from schemas.rss_schema import Article

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TranslatorAgent(BaseAgent):
    def run(self, article: Article) -> TranslationResult:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは翻訳の専門家です。英語の文章を自然な日本語に翻訳してください。"},
                    {"role": "user", "content": article.description or article.title}
                ]
            )
            translated_title = response.choices[0].message.content.strip()

            return TranslationResult(
                original=article,
                translated_title=translated_title,
                language="ja"
            )
        except Exception as e:
            print("❗ Error:", e)
            return TranslationResult(
                original=article,
                translated_title="翻訳に失敗しました。",
                language="ja"
            )
