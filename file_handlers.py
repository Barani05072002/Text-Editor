import io
import streamlit as st

# These variables should be imported from imports_setup.py in a real application
# They're included here for completeness
pdf_support = False
docx_support = False

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    if not pdf_support:
        st.error("PDF support is not available. Please install PyPDF2 with: pip install PyPDF2")
        return None
    
    try:
        import PyPDF2
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
        import docx
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