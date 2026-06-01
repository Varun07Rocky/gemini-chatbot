import streamlit as st
from google import genai
import os

# Set up the web page
# Set up the web page with Search Console meta tag tracking
st.set_page_config(
    page_title="Vaaris AI Chatbot - Personal AI Assistant", 
    page_icon="🤖", 
    layout="centered"
)

# This injects the Google verification tag cleanly into the header
st.markdown(
    f'<meta name="google-site-verification" content="raNnvSyzWIeR57e72376cvubq3WpxMbgWz0NCQmi5x0" />', 
    unsafe_allow_html=True
)
st.title("🤖 VAARIS")
st.caption("A sleek web app built with Streamlit and Google GenAI SDK")

# Initialize the Gemini Client using the secure secret key we saved
API_KEY = os.environ.get("GEMINI_API_KEY")

@st.cache_resource
def get_genai_client():
    return genai.Client(api_key=API_KEY)

client = get_genai_client()

# Initialize Chat Session with 2026 System Instructions AND Live Google Search
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": "You are a helpful assistant. The current year is 2026.",
            "tools": [{"google_search": {}}]  # This enables live internet search!
        }
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History on Re-run
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle New User Input
if user_input := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                response_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                response_placeholder.error(f"Error: {e}")
