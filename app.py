import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Clear any conflicting legacy environment variables
os.environ.pop("GOOGLE_API_KEY", None)

# 2. Fetch your key safely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")
    st.stop()

# 3. FORCE the client to use this key directly as a developer credential
# This stops the SDK from trying to validate it as an OAuth / Enterprise token
client = genai.Client(
    api_key=api_key,
    http_options={'headers': {'x-goog-api-key': api_key}}
)
