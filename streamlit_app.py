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
        border: 2px solid #808080;
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        max-width: 800px;
        background-color: transparent;
        text-align: center;
    }
    .chat-message {
        background-color: transparent;
        border: 1px solid #808080;
        border-radius: 10px;
        padding: 15px 15px 15px 50px;  /* Added left padding for icon */
        margin: 10px 0;
        transition: all 0.3s ease;
        position: relative;  /* For icon positioning */
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        background-color:transparent;
    }
    
    .chat-message::before {
        content: '';
        position: absolute;
        left: 15px;
        top: 50%;
        transform: translateY(-50%);
        width: 24px;
        height: 24px;
        background-size: contain;
        background-repeat: no-repeat;
    }
    
    .user-message::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23808080' stroke-width='2'%3E%3Ccircle cx='12' cy='8' r='5'/%3E%3Cpath d='M3 21v-2a7 7 0 0 1 7-7h4a7 7 0 0 1 7 7v2'/%3E%3C/svg%3E");
    }
    
    .assistant-message::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23808080' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpath d='M12 2a15 15 0 0 1 4 10 15 15 0 0 1-4 10 15 15 0 0 1-4-10 15 15 0 0 1 4-10z'/%3E%3C/svg%3E");
    }
    .verdict {
        font-weight: bold;
        margin-top: 10px;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.1);
    }
    .true {
        color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    .false {
        color: #F44336;
        border: 1px solid #F44336;
    }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle in container
st.markdown("""
    <div class="title-container">
        <h1>FAKEIT</h1>
        <p>Unmasking the Truth: Detecting Rumours Before They Spread!</p>
    </div>
""", unsafe_allow_html=True)

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
    st.session_state.messages.append({"role": "user", "content": prompt + "\n\nIs this information true or false?"})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = st.session_state.chat.send_message(prompt + "\n\nAnalyze if this information is true or false. Start your response with either 'TRUE:' or 'FALSE:' followed by your explanation.")
            
            # Extract verdict from response
            verdict = "TRUE" if response.text.upper().startswith("TRUE:") else "FALSE"
            verdict_class = "true" if verdict == "TRUE" else "false"
            
            # Display verdict and explanation
            st.markdown(f"""
                <div class="verdict {verdict_class}">{verdict}</div>
                <br>
                {response.text}
            """, unsafe_allow_html=True)
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response.text})