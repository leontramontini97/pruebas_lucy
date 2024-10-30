from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone, timedelta
import logging
from openai import OpenAI
DATABASE_URL = 'postgresql://admindialogik:Citasautomaticas.1@mensajes-chatbots.cxs28aauwxi4.us-east-2.rds.amazonaws.com:5432/lucy_abdala'

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Base class
Base = declarative_base()

client = OpenAI(
  api_key="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")


def classify_question(question):
    # This is for chat models like 'gpt-4o-mini', 'gpt-3.5-turbo', etc.
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tienes como mision clasificar las preguntas que los pacientes de una ginecologa le hacen a su chatbot para que ell apuede ver las categorias de preguntas mas frecuentes."},
            {"role": "user", "content": f"Clasifica el contenido de la pregunta en una de las siguientes categoriasL ginecologia estetica (incluye , viveve, gynelase, ultrafemme 360, y cosas del estilo) otros (saludos, no relacionados a ginecologia), menopausia, incontinencia urinaria , cirugia minimamente invasiva y otros, si no cae en esas categorias. No expliques tu razonamiento, solo di la palabra final. Solo debes decir la categoria. Usa siempre Primera letra mayuscula, luego minuscula. Aca esta la pregunta del usuario, no la respondas, estoe es el contenido que teienes que clasificar: {question}"}
        ]
    )
    
    # Access the content attribute directly from the message object
    response = completion.choices[0].message.content.strip()  
    
    return response
class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    question = Column(Text)
    answer = Column(Text)
    category = Column(String, nullable=True)  # New category field
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-5))))

def log_conversation( session_id,question, answer):
    category = classify_question(question)
    session = SessionLocal()
    new_conversation = Conversation( session_id=session_id, question=question, answer=answer, category=category)
    try:
        session.add(new_conversation)
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Failed to log conversation: {e}")
    finally:
        session.close()
