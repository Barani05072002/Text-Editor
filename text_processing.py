import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def simple_sentence_tokenize(text):
    """
    A simple sentence tokenizer that doesn't rely on NLTK.
    Uses regex to split text on sentence-ending punctuation followed by spaces.
    """
    # Split on period, exclamation mark, or question mark followed by space or newline
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Filter out empty sentences
    return [s.strip() for s in sentences if s.strip()]

def get_sentence_scores(sentences):
    if len(sentences) < 2:
        return [(0, 1.0)]
    
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(sentences)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return [(idx, sum(cosine_sim[idx]) - 1) for idx in range(len(sentences))]

def get_summary(sentences, sentence_scores, top_n=2):
    # Make sure top_n doesn't exceed the number of sentences
    top_n = min(top_n, len(sentences))
    
    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:top_n]
    sorted_sentences = sorted(sorted_sentences, key=lambda x: x[0])
    return ' '.join([sentences[idx] for idx, _ in sorted_sentences])