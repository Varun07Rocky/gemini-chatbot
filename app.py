import os
import streamlit as st
from google import genai

# 1. Page Configuration
st.set_page_config(page_title="Vaaris AI Chatbot", page_icon="🤖")
st.title("🤖 VAARIS")
st.caption("A sleek web app built with Streamlit and Google GenAI SDK")

# 2. Clear conflicting environment variables
os.environ.pop("GOOGLE_API_KEY", None)

# 3. Fetch key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")
    st.stop()

# 4. Initialize the Gemini Client
try:
    client = genai.Client(
        api_key=api_key,
        http_options={'headers': {'x-goog-api-key': api_key}}
    )
except Exception as e:
    st.error(f"Failed to initialize client: {e}")
    st.stop()

# 5. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User Input Area
if user_input := st.chat_input("Type your message here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate model response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Use the correct 2.5-flash model identifier for the new SDK
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input
            )
            response_text = response.text
            message_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            message_placeholder.error(f"Error generating response: {e}")
