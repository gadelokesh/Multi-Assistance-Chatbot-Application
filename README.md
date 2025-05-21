# Multi-Assistance Chatbot Streamlit App

## Overview
This is a **Streamlit-based Multi-Assistance Chatbot** app that leverages **LangChain** and **Google Gemini API** to provide various assistant roles. The chatbot can serve as:
- **Python Tutor**
- **Fitness Coach**
- **Travel Planner**
- **Career Advisor**
- **Mental Wellness Guide**
- **Code Assistant**

Users can interact with the chatbot by selecting their preferred role, and the chatbot will provide responses based on the selected role.

## Features
- **Multiple Assistance Roles**: Choose from a range of assistants for Python, Fitness, Travel, Career, Mental Wellness, and Code.
- **Google Gemini Integration**: The app uses **Google Gemini API** to provide real-time, accurate responses for various queries.
- **Dark-Themed UI**: A sleek, modern dark theme for enhanced user experience.
- **Responsive Design**: Built using Streamlit for an intuitive and responsive user interface.

## Live Demo
You can try out the app live here:  
https://multi-assistant-vwsttdlktlk4xvtnrrvq8r.streamlit.app/

## Sample Image of the App
![image](https://github.com/user-attachments/assets/adcd1587-604c-4cad-b0ab-62e8ae0f9b08)


## Installation
To run the app locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Darshanikant/Multi-Assistant.git
    cd Multi-Assistant
    ```

2. **Set up a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** (to store your API key):
    - In the `.env` file, add your **Google Gemini API Key**:
      ```
      GEMINI_API_KEY=your_api_key_here
      ```

5. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

6. The app should now be accessible at `http://localhost:8501`.

## Requirements
- Python 3.x
- Streamlit
- LangChain
- Google Generative AI (Gemini API)
- python-dotenv
- langchain_google_genai

## Usage
- Select a role from the options on the sidebar.
- Interact with the chatbot by typing your queries.
- The chatbot will provide a response based on the selected role.

# Thanks For Visiting
