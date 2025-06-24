from openai import OpenAI
import os
import numpy as np
from typing import List


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_to_english(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate the following text to English."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Translation Error:", e)
        return text  # fallback

def get_embedding(text: str) -> List[float]:
    try:
        res = client.embeddings.create(input=[text], model="text-embedding-3-small")
        return res.data[0].embedding
    except Exception as e:
        print("Embedding Error:", e)
        return [0.0] * 1536  # fallback

def cosine_similarity(vec1, vec2) -> float:
    a = np.array(vec1)
    b = np.array(vec2)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
