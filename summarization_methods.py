import streamlit as st
from transformers import pipeline
from text_processing import simple_sentence_tokenize, get_sentence_scores, get_summary

def abstractive_summary(text):
    # Handle texts that might be too long for the model
    max_chars = 1024 * 3  # Approximate character limit
    if len(text) > max_chars:
        text = text[:max_chars]
        st.warning("Text was truncated to fit within model limits.")
    
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def summarize(text, method="extractive", top_n=2):
    if not text.strip():
        return "No text to summarize."
    
    # Use our custom tokenizer instead of NLTK
    sentences = simple_sentence_tokenize(text)
    
    if method == "extractive":
        sentence_scores = get_sentence_scores(sentences)
        return get_summary(sentences, sentence_scores, top_n)
    elif method == "abstractive":
        return abstractive_summary(text)