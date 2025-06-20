from typing import List
from agents.base_agent import BaseAgent
from schemas.translation_schema import TranslationResult
from schemas.rss_schema import Article
from tools.translation_api import translate_text


class TranslatorAgent(BaseAgent):
    def __init__(self, target_lang: str = "JA"):
        self.target_lang = target_lang

    def run(self, input_data: List[Article]) -> List[TranslationResult]:
        translated = []

        for article in input_data:
            text_to_translate = article.title
            translated_text = translate_text(text_to_translate, target_lang=self.target_lang)

            result = TranslationResult(
                original=text_to_translate,
                translated=translated_text,
                lang=self.target_lang,
                metadata={
                    "source": article.source,
                    "url": article.url
                }
            )
            translated.append(result)

        return translated
