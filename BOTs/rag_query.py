from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os
from pathlib import Path

def ejecutar_consulta_rag(pregunta: str, persist_directory: str = "./chroma-data") -> str:
    """
    Recupera contexto desde Chroma y genera una respuesta con un modelo de lenguaje (RAG).
    
    Args:
        pregunta (str): La consulta del usuario.
        persist_directory (str): Ruta al directorio donde está almacenado Chroma.

    Returns:
        str: Respuesta generada por el modelo usando contexto documental.
    """
    # Leer clave de API
    api_key = os.getenv("OPENAI_API_KEY") or Path("OpenAI_key.txt").read_text().strip()

    # Embeddings (deben coincidir con los usados al indexar)
    embeddings = OpenAIEmbeddings(api_key=api_key)

    # Cargar base vectorial desde disco
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    # Crear un retriever (top 3 documentos más relevantes)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # Modelo de lenguaje
    llm = ChatOpenAI(temperature=0, openai_api_key=api_key)

    # Crear la cadena RAG con LangChain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True  # opcional, para debug o trazabilidad
    )

    # Ejecutar la consulta
    resultado = qa_chain({"query": pregunta})
    return resultado["result"]


if __name__ == "__main__":
    pregunta = "¿qué es la muerte maternal?"
    respuesta = responder_con_rag(pregunta)
    print(f"🤖 Respuesta: {respuesta}")

