import streamlit as st
import requests

def translate_text(text, target_language='ta'):
    """
    Translate text to the target language using Google Translate API (no key required).
    Default target language is Tamil ('ta').
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code (default: 'ta' for Tamil)
        
    Returns:
        str: Translated text or original text if translation fails
    """
    try:
        # Using a simple approach that works without authentication
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",  # Source language (auto-detect)
            "tl": target_language,  # Target language
            "dt": "t",  # Return text
            "q": text
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            # Extract translated text from response
            result = response.json()
            translated_text = ''.join([sentence[0] for sentence in result[0]])
            return translated_text
        else:
            st.error(f"Translation API error: Status code {response.status_code}")
            return text
    
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text  # Return original text if translation fails