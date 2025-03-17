import streamlit as st

# This must be the first Streamlit command
st.set_page_config(page_title="Text Summarizer", layout="centered")

# Import other libraries
import re
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

# Try importing optional dependencies for file handling
pdf_support = False
docx_support = False

with st.spinner("Checking available libraries..."):
    try:
        import PyPDF2
        pdf_support = True
    except ImportError:
        st.warning("PyPDF2 is not installed. PDF support is disabled. Install with: pip install PyPDF2")
    
    try:
        import docx
        docx_support = True
    except ImportError:
        st.warning("python-docx is not installed. DOCX support is disabled. Install with: pip install python-docx")