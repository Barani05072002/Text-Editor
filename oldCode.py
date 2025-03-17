import streamlit as st

# This must be the first Streamlit command
st.set_page_config(page_title="Text Summarizer", layout="centered")

# Import other libraries
import re
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

# Install required packages for handling different file types
# You'll need to run these commands in your terminal:
# pip install PyPDF2 python-docx

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

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    if not pdf_support:
        st.error("PDF support is not available. Please install PyPDF2 with: pip install PyPDF2")
        return None
    
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    if not docx_support:
        st.error("DOCX support is not available. Please install python-docx with: pip install python-docx")
        return None
    
    try:
        doc = docx.Document(io.BytesIO(file.getvalue()))
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {str(e)}")
        return None

def read_file(uploaded_file):
    """Read text from various file formats."""
    try:
        if uploaded_file.type == "text/plain":
            # For text files
            return uploaded_file.getvalue().decode("utf-8")
        
        elif uploaded_file.type == "application/pdf" and pdf_support:
            # For PDF files
            return extract_text_from_pdf(uploaded_file)
        
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                                    "application/msword"] and docx_support:
            # For DOCX and DOC files
            return extract_text_from_docx(uploaded_file)
        
        else:
            st.error(f"Unsupported file type: {uploaded_file.type}. Please upload a .txt, .pdf, or .docx file.")
            return None
    
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

# Streamlit UI
st.title("📄 Text Summarizer")
st.markdown("Enhance your reading experience with AI-powered text summarization.")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Text Input", "File Upload"])

with tab1:
    text_input = st.text_area("Enter the text to summarize:", height=250)
    
with tab2:
    accepted_types = ["txt"]
    if pdf_support:
        accepted_types.append("pdf")
    if docx_support:
        accepted_types.extend(["docx", "doc"])
    
    uploaded_file = st.file_uploader(f"Upload a file ({', '.join(accepted_types)})", type=accepted_types)
    file_text = None
    
    if uploaded_file is not None:
        with st.spinner("Reading file..."):
            file_text = read_file(uploaded_file)
        
        if file_text:
            st.success("File successfully loaded!")
            with st.expander("Preview uploaded text"):
                st.write(file_text[:500] + "..." if len(file_text) > 500 else file_text)

# Determine which text to use (input or file)
text_to_summarize = ""
if tab2._active and file_text:
    text_to_summarize = file_text
else:
    text_to_summarize = text_input

# Summarization options
st.subheader("Summarization Options")
col1, col2 = st.columns(2)

with col1:
    method = st.radio("Select summarization method:", ["extractive", "abstractive"])

with col2:
    top_n = st.slider("Number of key sentences (extractive only):", 1, 10, 2)

if st.button("Summarize"):
    if text_to_summarize.strip():
        with st.spinner("Generating summary..."):
            try:
                summary = summarize(text_to_summarize, method, top_n)
                
                st.subheader("🔹 Summary:")
                st.write(summary)
                
                # Calculate reduction percentage
                original_word_count = len(text_to_summarize.split())
                summary_word_count = len(summary.split())
                reduction = round((1 - summary_word_count / original_word_count) * 100, 1)
                
                st.success(f"Reduced text by {reduction}% (from {original_word_count} to {summary_word_count} words)")
            except Exception as e:
                st.error(f"An error occurred during summarization: {str(e)}")
                st.info("Error details: " + str(e))
    else:
        st.warning("Please enter some text or upload a file to summarize.")

st.markdown("---")
st.info("Breathe In...Breathe Out...")