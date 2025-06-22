# tools/chroma_store.py

import chromadb
from chromadb.config import Settings
from schemas.translation_schema import TranslationResult

client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection(name="translations")

def save_translation(result: TranslationResult):
    collection.add(
        documents=[result.translated_text],
        metadatas=[{
            "title": result.original.title,
            "url": result.original.link
        }],
        ids=[result.original.title]
    )

def find_similar(title: str, top_k: int = 3):
    return collection.query(
        query_texts=[title],
        n_results=top_k
    )
