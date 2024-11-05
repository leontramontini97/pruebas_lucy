import streamlit as st
import time
import uuid
import os
import logging
from utils import retriever, get_session_history, rag_chain
from langchain_core.runnables.history import RunnableWithMessageHistory




# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # You can change this to DEBUG or ERROR as needed
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

SESSION_TIMEOUT = 1800  # 30 minutes


def reset_session():
    """Reset the session state, including session ID, messages, and interaction time."""
    st.session_state.clear()
    st.session_state.session_id = str(uuid.uuid4())  # Create a new session ID
    st.session_state.messages = []  # Reset chat history
    st.session_state.last_interaction = time.time()  # Reset last interaction time


# Initialize session if not set or reset if session timed out
if 'session_id' not in st.session_state:
    reset_session()

else:
    # Initialize last interaction time if it's not already set
    current_time = time.time()
    last_interaction = st.session_state.get('last_interaction', current_time)
    
    if current_time - last_interaction > SESSION_TIMEOUT:
        # Reset session if the user has been inactive for longer than the timeout
        reset_session()
    else:
        # Update the last interaction time
        st.session_state.last_interaction = current_time





# Setup page configuration
st.set_page_config(page_title="LUCY", layout="wide", page_icon='💕')
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Titles and Main Heading

st.markdown(
    """
    <div style='text-align: center;'>
        <h2> Hola! Soy LUCY AI </h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# Adding margin or padding to create space between the lines
st.markdown(
    """
    <div style='text-align: center; width: 300px; height: 300px; display: flex; align-items: center; justify-content: center; margin: 30px auto; border: 1px solid #ccc;'>
        <h5> Tu Asistente Virtual con 
Inteligencia Artificial 
Estoy aquí para resolver tus dudas 
y responder a tus preguntas! </h5>
    </div>
    """,
    unsafe_allow_html=True,
)


# Sidebar functionalities
def sidebar():
    
    st.sidebar.image('logo_lucy_3.jpeg', use_column_width=True)
    

    # Further Assistance Information
    st.sidebar.markdown("###  ¿Necesitas más información?")
       
    st.sidebar.markdown(
            """
             📞 Estética Íntima: wa.me/573106391610  \n
             📞 Ginecología: wa.me/573106336514  

             📪 lucyabdala@gmail.com \n
             
             💻 https://ginecologalucyabdala.com/

             📍 Clínica Portoazul Aúna Cons. 414 
                Barranquilla, Colombia 


            """
        )
    st.sidebar.markdown(
    """
    ---
    <div style='font-size: 12px;'>  <!-- Adjust the font size here -->
        <strong> Disclaimer :</strong> <br>
        Esta información es proporcionada por un asistente virtual para fines educativos. 
        No sustituye el consejo médico profesional. 
        Para una evaluación médica adecuada, consulta a tu médico.
    </div>
    """,
    unsafe_allow_html=True
)
    

    st.sidebar.markdown(
    """
    <div style='text-align: center; margin-top: 18px;'>
        <p style='color: gray;'> 2024, Made with 🖤 by Dialogik.co </p>
    </div>
    """,
    unsafe_allow_html=True
)
    # Disclaimer in Sidebar
    


# Main chat application
def chat():
    

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field for user input
    user_message = st.chat_input("Escribe tu mensaje aquí...")

    if user_message:
        # Store and display the user message
        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

      
        common_responses = {
    "hola": "Bienvenida a Lucy AI, Asistente Virtual con Inteligencia Artificial de la Dra. Lucy Abdala para ofrecerte mayor información con respecto a temas de tu Salud, Bienestar, Sexualidad y Estética Íntima Femenina.",
    "adiós": "¡Hasta luego! Espero haberte ayudado. 👋 👋 👋 👋",
    "gracias": "¡Con gusto! Si tienes otra consulta, estoy aquí para ayudarte 😊",
    "¿cómo estás?": "¡Estoy funcionando al 100%! 🤖 ¿En qué puedo ayudarte?",
    "¿quién te creó?": "Fui creado por Dialogik, un equipo de expertos en tecnología y automatización para ayudarte en todo lo que necesites 📚🔧. Las respuestas que ves acá son basadas en la información de la página web de la Dra Abdala. Sin embargo, si se trata de una consulta médica, es mejor que la consultes directamente a ella. Soy un sistema de Ineligencia artificial y puedo cometer errores.",
    "¿cuál es tu nombre?": "Mi nombre es Asistente virtual de la doctora Lucy Abdala 🤖, tu asistente virtual siempre disponible para ayudarte.",
    "¿qué puedes hacer?": "Estoy entrenado para responder preguntas que puedas tener en relación con la preparación para cirugías para que estés lo mejor informado posible!",
    "¿eres un robot?": "Sí, soy un robot asistente virtual diseñado para ayudarte con información y consultas 👾",
    "¿trabajas las 24 horas?": "¡Así es! Estoy disponible las 24 horas del día, los 7 días de la semana, siempre listo para ayudarte 💪",}




        response_text = common_responses.get(user_message.lower(), None)
        if response_text:
            with st.chat_message("assistant"):
                st.markdown(response_text)
        else:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()  # Placeholder for the response
                response_placeholder.markdown("🤔 Estoy pensando...")

            try:
                print("I should see this in the terminal")
                logging.debug(f"Hello, I am trapped inside your program")
                conversational_rag_chain = RunnableWithMessageHistory(
                    rag_chain,
                    get_session_history,
                    input_messages_keys='input',
                    history_messages_key='chat_history',
                    output_messages_key='answer'
                )
                docs = retriever.invoke(user_message)

                if not docs:
                    raise ValueError("No documents found by retriever.")

                context_text = "\n\n".join([doc.page_content for doc in docs])

                response = conversational_rag_chain.invoke(
                    {"context": context_text, "input": user_message},
                    config={"configurable": {"session_id": st.session_state.session_id}}
                )

                if 'answer' not in response:
                    raise KeyError("Response missing 'answer' key.")
                
                response_text = response.get('answer')
            except KeyError as ke:
                logging.error(f"KeyError encountered: {ke}")
                response_text = "En el momento estamos expermientando algunos problemas 💔 . Volveremos a estar disponibles en breve."
            except ValueError as ve:
                logging.error(f"ValueError encountered: {ve}")
                response_text = "En el momento estamos expermientando algunos problemas 💔 . Volveremos a estar disponibles en breve."

            except Exception as e:
                logging.error(f"An unexpected error occurred: {str(e)}")
                response_text = "En el momento estamos expermientando algunos problemas 💔 . Volveremos a estar disponibles en breve."
                # Display the assistant's response
                
            
            response_placeholder.markdown(response_text)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
      

    # Add disclaimer at the bottom of the chat if no messages yet
    
    if len(st.session_state.messages)== 0:
        st.markdown(
        """
        ---
        **Disclaimer:**  
        Las respuestas proporcionadas por este asistente virtual son de carácter informativo y no reemplazan una consulta médica. Para un diagnóstico o tratamiento adecuado, por favor consulta a la Dra. Lucy Abdala.
        """
        )
    
    
# Main App
def main():
    sidebar()  # Load the sidebar functionalities
    chat()  # Load the main chat interface

if __name__ == "__main__":
    main()
