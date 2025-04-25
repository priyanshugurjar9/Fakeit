import streamlit as st
import google.generativeai as genai

# Configure API key
API_KEY = "AIzaSyC-JTDfvsKY9Vt_GyDg_LeF6nOXJ-gT_O8"
genai.configure(api_key=API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Set page configuration
st.markdown("""
    <style>
    .title-container {
        border: 2px solid black;
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        max-width: 800px;
        background-color: transparent;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle in container
st.markdown("""
    <div class="title-container">
        <h1> FAKEIT</h1>
        <p>Unmasking the Truth: Detecting Rumours Before They Spread!</p>
    </div>
""", unsafe_allow_html=True)

# Add header


# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your mis/info here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})