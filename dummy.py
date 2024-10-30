
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

import plotly.express as px

#######################
# Database setup using SQLAlchemy

DATABASE_URL = 'postgresql://admindialogik:Citasautomaticas.1@mensajes-chatbots.cxs28aauwxi4.us-east-2.rds.amazonaws.com:5432/lucy_abdala'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Load data from the 'conversations' table
def load_conversations():
    query = "SELECT id, question AS message_body, answer AS response, category, timestamp, session_id FROM conversations"
    df = pd.read_sql(query, engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  # Convert to datetime
    return df

#######################
# Login functionality

USERNAME = "admin.lucyabdala"
PASSWORD = "Solucionesinteligentes.2024"

def login():
    """Handle the login form."""
    st.title("Login")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        st.write("Ya has iniciado sesión. Ve al panel de mensajes.")
    else:
        username = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Login"):
            if username == USERNAME and password == PASSWORD:
                st.session_state["logged_in"] = True
                st.write("Inicio de sesión exitoso!")
                time.sleep(1)
                st.rerun()  
            else:
                st.error("Credenciales incorrectas")

# Logout functionality
def logout():
    """Handle the logout action."""
    st.session_state["logged_in"] = False
    st.rerun()

#######################
# Main dashboard functionality

def display_dashboard():
    """Display the main message dashboard if logged in."""
    st.title("Mensajes Recibidos")

    # Load messages from the database
    df_messages = load_conversations()

    if not df_messages.empty:
        st.markdown("### Último Mensaje")
        latest_message = df_messages.iloc[-1]

        # Adjust the timestamp for UTC-5
        timestamp_utc5 = latest_message['timestamp'] - timedelta(hours=5)

        st.markdown(f"""
         <div>
            <p style='font-size:14px;'><strong>Mensaje:</strong> {latest_message['message_body']}</p>
            <p style='font-size:14px;'><strong>Fecha y Hora:</strong> {timestamp_utc5.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    """, unsafe_allow_html=True)

    else:
        st.write("No hay mensajes disponibles en este momento.")

    # Display messages table
    st.markdown("### Tabla con mensajes ")

    # Ensure correct order of columns and rename for display
    df_messages = df_messages[['id', 'message_body', 'response', 'category', 'timestamp', 'session_id']]  # Reorder columns

    # Adjust timestamp and subtract 5 hours
    df_messages['timestamp'] = df_messages['timestamp'] - timedelta(hours=5)

    # Format the timestamp for display
    df_messages['timestamp'] = df_messages['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Display the DataFrame with the correct column mapping
    st.dataframe(df_messages, hide_index=True, column_config={
        "id": st.column_config.TextColumn("ID"),
        "message_body": st.column_config.TextColumn("Mensaje"),
        "response": st.column_config.TextColumn("Respuesta"),
        "timestamp": st.column_config.TextColumn("Fecha y Hora"),
        "session_id": st.column_config.TextColumn("Session ID"),
    })

    # Fill any missing categories
    df_messages['category'] = df_messages['category'].fillna('Desconocido')

    category_counts = df_messages['category'].value_counts()

    fig = px.pie(values=category_counts.values, names=category_counts.index, title="Distribución de Categorías de Preguntas")
    st.plotly_chart(fig)

    st.markdown("### Todos los mensajes ")
    # Sort by index in descending order
    df_messages_sorted = df_messages.sort_values(by='timestamp', ascending=False)

    # Iterate over the sorted DataFrame
    for idx, row in df_messages_sorted.iterrows():
        # Adjust the timestamp for each row
        row_timestamp_utc5 = row['timestamp']

        with st.expander(f"Mensaje {row['id']}"):
            st.write(f"**Pregunta:** {row['message_body']}")
            st.write(f"**Respuesta:** {row['response']}")
            st.write(f"**Categoría:** {row['category']}")
            st.write(f"**Fecha y Hora:** {row_timestamp_utc5}")

    # Sidebar for logout and logo
    with st.sidebar:
        st.sidebar.image('logo_lucy_3.jpeg', use_column_width=True)
        st.title("Panel de Mensajes")

        if st.button("Cerrar sesión"):
            logout()

        st.sidebar.markdown("""
        <div style='text-align: center; margin-top: 18px;'>
            <p style='color: gray;'>Made with 🖤 by Dialogik.co, 2024. </p>
        </div>
        """, unsafe_allow_html=True)

#######################
# Main Streamlit app

# Page configuration
st.set_page_config(
    page_title="Panel de Mensajes",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check login status and show the appropriate page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()  # Show login form if not logged in
else:
    display_dashboard()  # Show message dashboard if logged in
