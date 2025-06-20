from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(text1: str, text2: str) -> float:
    """
    2つのテキスト間のコサイン類似度を計算する。
    類似度は 0.0〜1.0 の範囲で返され、高いほど類似している。
    """
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]
