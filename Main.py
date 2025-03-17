import streamlit as st
from imports_setup import pdf_support, docx_support
from summarization_methods import summarize
from file_handlers import read_file
from translation_service import translate_text

# Streamlit UI
st.title("📄 Text Summarizer")
st.markdown("Enhance your reading experience with AI-powered text summarization.")

# Initialize session state variables
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'translated_summary' not in st.session_state:
    st.session_state.translated_summary = ""
if 'summary_generated' not in st.session_state:
    st.session_state.summary_generated = False

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

# Summarize button functionality
if st.button("Summarize"):
    if text_to_summarize.strip():
        with st.spinner("Generating summary..."):
            try:
                summary = summarize(text_to_summarize, method, top_n)
                
                # Store in session state
                st.session_state.summary = summary
                st.session_state.translated_summary = ""  # Reset translated summary
                st.session_state.summary_generated = True
                
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

# Display summary section
if st.session_state.summary_generated:
    st.subheader("🔹 Summary:")
    st.write(st.session_state.summary)
    
    # Translation button
    if st.button("Translate to Tamil"):
        with st.spinner("Translating to Tamil..."):
            translated_text = translate_text(st.session_state.summary)
            st.session_state.translated_summary = translated_text
    
    # Display translation if available
    if st.session_state.translated_summary:
        st.subheader("🔹 Tamil Translation:")
        st.write(st.session_state.translated_summary)

st.markdown("---")
st.info("Breathe In...Breathe Out...")