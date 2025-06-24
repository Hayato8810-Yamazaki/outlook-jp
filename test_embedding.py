from tools.embedding_utils import get_embedding, cosine_similarity
from tools.translation_api import translate_to_english  # あれば

text1 = "Prime Minister Kishida visits the US"
text2_ja = "岸田首相がアメリカを訪問"

text2 = translate_to_english(text2_ja)  # 英語に翻訳
emb1 = get_embedding(text1)
emb2 = get_embedding(text2)

sim = cosine_similarity(emb1, emb2)
print(f"Cosine similarity after translation: {sim:.3f}")
