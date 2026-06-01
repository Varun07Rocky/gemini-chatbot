import streamlit as st
from google import genai

# Set up the web page
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 My Gemini AI Chatbot")
st.caption("A sleek web app built with Streamlit and Google GenAI SDK")

# 1. Initialize the Gemini Client
# For security, you can pull your key from your AI Studio dashboard:
API_KEY = "AQ.Ab8RN6I8nXiZ4VOBXZ4KZwqstROlP5ffQxp1QgFZYVOTQhbqWg" 

@st.cache_resource
def get_genai_client():
    return genai.Client(api_key=API_KEY)

client = get_genai_client()

# 2. Initialize Chat Session in Streamlit's Memory
if "chat_session" not in st.session_state:
    # This starts a continuous conversation tracking session
    st.session_state.chat_session = client.chats.create(model="gemini-2.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History on Re-run
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle New User Input
if user_input := st.chat_input("Type your message here..."):
    # Display user message instantly
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate response from Gemini
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                # Send the message using the active session tracking
                response = st.session_state.chat_session.send_message(user_input)
                response_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                response_placeholder.error(f"Error: {e}")