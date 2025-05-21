import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
load_dotenv()

# Define assistant profiles with dark theme colors
ASSISTANT_PROFILES = {
    "🐍 Python Tutor": {
        "description": "An expert Python programming tutor who explains concepts with simple code examples.",
        "color": "#4B8BBE",  # Python blue
        "icon": "🐍",
        "accent_color": "#FFD43B"  # Python yellow
    },
    "💪 Fitness Coach": {
        "description": "A professional fitness expert providing personalized workout routines and nutrition advice.",
        "color": "#FF5252",  # Bright red
        "icon": "💪",
        "accent_color": "#69F0AE"  # Mint green
    },
    "✈️ Travel Planner": {
        "description": "A travel specialist helping you plan trips, recommend places, and give practical travel advice.",
        "color": "#40C4FF",  # Bright blue
        "icon": "✈️",
        "accent_color": "#FFAB40"  # Orange
    },
    "💼 Career Advisor": {
        "description": "A career counselor offering resume tips, interview preparation, and strategic career planning.",
        "color": "#B388FF",  # Purple
        "icon": "💼",
        "accent_color": "#EA80FC"  # Pink
    },
    "🧠 Mental Wellness Guide": {
        "description": "A supportive wellness coach providing kind advice on managing stress and emotions.",
        "color": "#64FFDA",  # Teal
        "icon": "🧠",
        "accent_color": "#80D8FF"  # Light blue
    },
    "💻Code Assistant": {
        "description": "A coding assistant that helps you with programming tasks and debugging.",
        "color": "#FF6F00",  # Orange
        "icon": "💻",
        "accent_color": "#FFD600"  # Yellow
    },
}

# Streamlit config
st.set_page_config(
    page_title="Multi-Assistance Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme styling
st.markdown("""
<style>
    /* Base styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark theme core */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Sidebar styling */
    header[data-testid="stHeader"] {
        background-color: #121212;
        border-bottom: 1px solid #2d2d2d;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #2d2d2d;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #1e1e1e;
        padding: 1rem;
    }
    
    /* Fixing streamlit elements for dark mode */
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #3d3d3d;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6e6e6e;
        box-shadow: 0 0 0 2px rgba(110, 110, 110, 0.3);
    }
    
    .stRadio > div {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 8px;
    }
    
    /* Main header */
    .main-header {
        position: sticky;
        background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid #3d3d3d;
    }
    
    
    .main-header h1 {
        color: #e0e0e0;
        font-weight: 700;
        margin: 0;
        font-size: 2.2rem;
    }
    
    .main-header p {
        color: #b0b0b0;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    
    
    /* Message styling */
    .user-message {
        background-color: #2d2d2d;
        color: #e0e0e0;
        padding: 12px 18px;
        border-radius: 18px 18px 0 18px;
        margin: 16px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        line-height: 1.5;
    }
    
    .bot-message {
        background-color: #252525;
        color: #e0e0e0;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 0;
        margin: 16px 0;
        max-width: 80%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        line-height: 1.5;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        padding: 12px 18px;
        align-items: center;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background-color: #b0b0b0;
        border-radius: 50%;
        margin: 0 2px;
        animation: typing-animation 1.4s infinite ease-in-out;
    }
    
    @keyframes typing-animation {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-5px); }
    }
    
    /* Input container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1a1a1a;
        padding: 15px 20px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.4);
        z-index: 999;
        display: flex;
        align-items: center;
        border-top: 1px solid #2d2d2d;
    }
    
    /* Assistant card styling */
    .assistant-card {
        background-color: #252525;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        border: 1px solid #3d3d3d;
    }
    
    .assistant-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #3d3d3d;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #3d3d3d;
        border-color: #4d4d4d;
        transform: translateY(-2px);
    }
    
    /* API key container */
    .api-key-container {
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid #3d3d3d;
    }
    
    /* Assistant chat title */
    .assistant-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid;
    }
    
    
    .profile-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        border-color: #4d4d4d;
    }
    
    .profile-icon {
        font-size: 2rem;
        margin-bottom: 15px;
    }
    
    /* Instructions container */
    .instructions-container {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        border: 1px solid #3d3d3d;
        margin-top: 30px;
    }
    
    /* App footer */
    .app-footer {
        text-align: center;
        color: #8e8e8e;
        font-size: 12px;
        margin-top: 30px;
        margin-bottom: 100px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3d3d3d;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4d4d4d;
    }
    
    /* Link styling */
    a {
        color: #40C4FF;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "model" not in st.session_state:
    st.session_state.model = None
if "activated" not in st.session_state:
    st.session_state.activated = False
if "thinking" not in st.session_state:
    st.session_state.thinking = False
if "assistant_name" not in st.session_state:
    st.session_state.assistant_name = ""
if "user_input_text" not in st.session_state:
    st.session_state.user_input_text = ""
with st.sidebar:
    st.markdown("<h2>🔧 Assistant Setup</h2>", unsafe_allow_html=True)

    # Assistant selection
    st.markdown("### Choose your assistant")

    # Create radio buttons for assistant selection
    assistant = st.selectbox(
        "Select an assistant:",
        list(ASSISTANT_PROFILES.keys()),
        label_visibility="collapsed",
        key="assistant_select",
        on_change=lambda: st.session_state.update(chat_history=[SystemMessage(content=ASSISTANT_PROFILES[st.session_state.assistant_select]["description"])] if st.session_state.get("activated") else [], activated=False, model=None, thinking=False, assistant_name=st.session_state.assistant_select, user_input_text="")
    )

    # Display selected assistant info
    profile = ASSISTANT_PROFILES[assistant]
    st.markdown(
        f"""
        <div style='background-color: #252525;
                        padding: 15px;
                        border-radius: 10px;
                        border-left: 4px solid {profile['color']};
                        margin: 10px 0 20px 0;
                        border: 1px solid #3d3d3d;'>
            <div style='font-size: 2rem; margin-bottom: 10px;'>{profile['icon']}</div>
            <h3 style='color: {profile['color']}; margin: 0;'>{assistant}</h3>
            <p style='margin-top: 8px; font-size: 14px; color: #b0b0b0;'>{profile['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # API key input
    st.markdown("### API Configuration")
    with st.container():
        st.markdown(
            """
            <div class='api-key-container'>
                <p style='font-size: 14px; margin-bottom: 10px; color: #b0b0b0;'>
                    Enter your Gemini API key to activate the assistant
                </p>
            """,
            unsafe_allow_html=True
        )
        user_api_key = st.text_input("Gemini API Key:", type="password", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    # Activate button
    activate = st.button("🚀 Activate Assistant", use_container_width=True)
    # Refresh chat button
    if st.session_state.activated:
        if st.button("🔄 Refresh Chat", use_container_width=True):
            st.session_state.chat_history = [SystemMessage(content=ASSISTANT_PROFILES[st.session_state.assistant_name]["description"])]
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 12px; color: #8e8e8e;'>
            <p>Your API key is used only for this session and is not stored.</p>
            <p>© 2025 Multi-Assistance Chatbot</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Activate assistant
if activate and user_api_key:
    try:
        st.session_state.chat_history = [SystemMessage(content=ASSISTANT_PROFILES[assistant]["description"])]
        st.session_state.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=user_api_key,
            temperature=0.7
        )
        st.session_state.activated = True
        st.session_state.assistant_name = assistant
        st.toast("✅ Assistant activated successfully!", icon="🎉")
    except Exception as e:
        st.error(f"Failed to activate assistant: {str(e)}")

# Main content area
if st.session_state.activated:
    # Header
    st.markdown(
        f"""
        <div class='main-header'>
            <h1>Your {assistant} Chatbot</h1>
            <p>Your personal AI assistant powered by Google Gemini</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Assistant title
    profile = ASSISTANT_PROFILES[assistant]
    st.markdown(
        f"""
        <div class='assistant-title' style='color: {profile['color']};'>
            {profile['icon']} Chatting with your {assistant}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Chat area
    chat_container = st.container()
    with chat_container:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

        # Welcome message if chat is empty
        if len(st.session_state.chat_history) <= 1:  # Only system message
            st.markdown(
                f"""
                <div class='bot-message' style='border-left: 3px solid {profile['color']};'>
                    <strong style='color: {profile['color']};'>{profile['icon']} {assistant.split(" ", 1)[1]}:</strong>
                    Hello! I'm your {assistant.split(" ", 1)[1]}. How can I help you today?
                </div>
                """,
                unsafe_allow_html=True
            )

        # Display chat history
        for msg in st.session_state.chat_history:
            if isinstance(msg, HumanMessage):
                st.markdown(
                    f"""
                    <div class='user-message' style='border-right: 3px solid {profile['accent_color']};'>
                        <strong style='color: {profile['accent_color']};'>You:</strong> {msg.content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif isinstance(msg, AIMessage):
                st.markdown(
                    f"""
                    <div class='bot-message' style='border-left: 3px solid {profile['color']};'>
                        <strong style='color: {profile['color']};'>{profile['icon']} {assistant.split(" ", 1)[1]}:</strong> {msg.content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Typing indicator
        if st.session_state.thinking:
            st.markdown(
                f"""
                <div class='bot-message' style='background-color: transparent; box-shadow: none; border-left: 3px solid {profile['color']};'>
                    <strong style='color: {profile['color']};'>{profile['icon']} {assistant.split(" ", 1)[1]}:</strong>
                    <div class='typing-indicator'>
                        <div class='typing-dot'></div>
                        <div class='typing-dot'></div>
                        <div class='typing-dot'></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # Message handler
    def handle_send():
        if st.session_state.user_input_text.strip():
            st.session_state.chat_history.append(HumanMessage(content=st.session_state.user_input_text))
            st.session_state.thinking = True
            st.session_state.user_input_text = ""
            #st.rerun()

    # Input area
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Type your message...",
            key="user_input_text",
            label_visibility="collapsed",
            placeholder=f"Message your {assistant.split(' ', 1)[1]}...",
            on_change=handle_send
        )
    with col2:
        send_button = st.button("Send", key="send_button", use_container_width=True, on_click=handle_send)

    # Process the response
    if st.session_state.thinking:
        try:
            with st.spinner(""):
                response = st.session_state.model.invoke(st.session_state.chat_history)
                st.session_state.chat_history.append(AIMessage(content=response.content))
                st.session_state.thinking = False
                st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.thinking = False

# Welcome screen
else:
    # Header
    st.markdown(
        """
        <div class='main-header'>
            <h1>✨ Multi-Assistant Chatbot</h1>
            <p>Your personal AI assistant powered by Google Gemini</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Welcome message
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2>Welcome to Multi-Assistant Chatbot!</h2>
            <p>Select an assistant and enter your API key in the sidebar to get started.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display assistant cards in a grid
    st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
    cols = st.columns(3)

    for i, (name, profile) in enumerate(ASSISTANT_PROFILES.items()):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class='profile-card' style='border-top: 5px solid {profile["color"]};'>
                    <div class='profile-icon' style='color: {profile["color"]};'>{profile["icon"]}</div>
                    <h3 style='color: {profile["color"]};'>{name}</h3>
                    <p style='font-size: 14px; color: #b0b0b0;'>{profile["description"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # Instructions
    st.markdown(
        """
        <div class='instructions-container'>
            <h3 style='text-align: center;'>Getting Started</h3>
            <ol style='padding-left: 30px; color: #b0b0b0;'>
                <li>Select an assistant from the sidebar that matches your needs</li>
                <li>Enter your Google Gemini API key in the provided field</li>
                <li>Click the "Activate Assistant" button to start chatting</li>
            </ol>
            <p style='font-size: 14px; color: #8e8e8e; margin-top: 20px; text-align: center;'>
                Don't have a Gemini API key? <a href="https://ai.google.dev/" target="_blank">Get one here</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Footer
    st.markdown(
        """
        <div class='app-footer'>
            <p>Devoloped By L © 2025 | All Rights Reserved</p>
        </div>
        """,
        unsafe_allow_html=True
    )
