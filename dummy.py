import streamlit as st
import time
import uuid
import os
import logging
from utils import retriever, get_session_history, rag_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from PIL import Image
import re

def sanitize_text(text):
    # Remove HTML tags, excessive whitespace, and special characters
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)  # Remove extra whitespace
    clean_text = clean_text.strip()  # Trim leading/trailing whitespace
    return clean_text

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

SESSION_TIMEOUT = 1800  # 30 minutes

def reset_session():
    st.session_state.clear()
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.last_interaction = time.time()

if 'session_id' not in st.session_state:
    reset_session()
else:
    current_time = time.time()
    last_interaction = st.session_state.get('last_interaction', current_time)
    if current_time - last_interaction > SESSION_TIMEOUT:
        reset_session()
    else:
        st.session_state.last_interaction = current_time

st.set_page_config(page_title="LUCY", layout="wide", page_icon='👩‍⚕️')
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

with st.container():
    cols = st.columns(9)
    with cols[4]:
        st.image("logo_lucy_este.png", use_column_width=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            """
            <div style='text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: -10px; padding: 0px; width: 100%;'>
                <h2>Hola! Soy LUCY AI</h2>
                <h5>Tu Asistente Virtual con </h5>  
                <h5>Inteligencia Artificial </h5> 
                <h5>Estoy aquí para resolver tus dudas!</h5>
            </div>
            """,
            unsafe_allow_html=True
        )

def sidebar():
    st.sidebar.markdown("###  ¿Necesitas más información?")
    st.sidebar.markdown(
    """
    ▶️ <a href="https://wa.me/573106391610" target="_blank">Estética Íntima</a>  <br>
    ▶️ <a href="https://wa.me/573106336514" target="_blank">Ginecología</a>  <br>
    ▶️ lucyabdala@gmail.com  <br>
    ▶️ [ginecologalucyabdala.com](https://ginecologalucyabdala.com/)  <br>
    📍 Clínica Portoazul Aúna Cons. 414 Barranquilla, Colombia
    """, unsafe_allow_html=True)
    st.sidebar.markdown(
    """
    ---
    <div style='font-size: 16px;'>
        <strong> Disclaimer:</strong> <br>
        Esta información es proporcionada por un asistente virtual para fines educativos. 
        No sustituye el consejo médico profesional. 
        Para una evaluación médica adecuada, consulta a tu médico.
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown(
    """
    <div style='text-align: center; margin-top: 18px;'>
        <p style='color: gray;'>2024, Made with 🖤 by Dialogik.co</p>
    </div>
    """, unsafe_allow_html=True)

def chat():
    inline_style = "font-size: 18px !important; line-height: 1.6 !important; font-family: Arial, sans-serif !important; font-weight: normal !important;"

    st.markdown(
    """<style> 
    .response-text { 
        font-size: 18px !important; 
        line-height: 1.6 !important;
        font-family: Arial, sans-serif !important;
        font-weight: normal !important;
    } 
    </style>""",
    unsafe_allow_html=True
    )
  
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            sanitized_content = sanitize_text(message["content"])
            st.markdown(f"<div style='{inline_style}'>{sanitized_content}</div>", unsafe_allow_html=True)

    user_message = st.chat_input("Escribe tu mensaje aquí...")

    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(f"<div style='{inline_style}'>{user_message}</div>", unsafe_allow_html=True)

        response_text = "Generated or predefined response here"
        if response_text:
            with st.chat_message("assistant"):
                st.markdown(f"<div style='{inline_style}'>{sanitize_text(response_text)}</div>", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": response_text})

def main():
    sidebar()
    chat()

if __name__ == "__main__":
    main()
