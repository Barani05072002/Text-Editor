import streamlit as st
from transformers import pipeline
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Download NLTK data
nltk.download('punkt')

def tokenize_text(text):
    tokenizer_path = "C:/Users/Vebbox/nltk_data/tokenizers/punkt/english.pickle"
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)
    return tokenizer.tokenize(text)

def get_sentence_scores(sentences):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(sentences)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return [(idx, sum(cosine_sim[idx]) - 1) for idx in range(len(sentences))]

def get_summary(sentences, sentence_scores, top_n=2):
    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:top_n]
    sorted_sentences = sorted(sorted_sentences, key=lambda x: x[0])
    return ' '.join([sentences[idx] for idx, _ in sorted_sentences])

def abstractive_summary(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def summarize(text, method="extractive", top_n=2):
    sentences = tokenize_text(text)
    if method == "extractive":
        sentence_scores = get_sentence_scores(sentences)
        
        return get_summary(sentences, sentence_scores, top_n)
    elif method == "abstractive":
        return abstractive_summary(text)

# Streamlit UI
st.set_page_config(page_title="Text Summarizer", layout="centered")
st.title("📄 Text Summarizer")
st.markdown("Enhance your reading experience with AI-powered text summarization.")

text = st.text_area("Enter the text to summarize:")
method = st.radio("Select summarization method:", ["extractive", "abstractive"], horizontal=True)
top_n = st.slider("Select number of key sentences (only for extractive method):", 1, 5, 2)

if st.button("Summarize"):
    if text.strip():
        summary = summarize(text, method, top_n) if method == "extractive" else summarize(text, method)
        st.subheader("🔹 Summary:")
        st.write(summary)

    else:
        st.warning("Please enter some text to summarize.")

st.markdown("---")
st.info("Breath In...Breath Out...")
