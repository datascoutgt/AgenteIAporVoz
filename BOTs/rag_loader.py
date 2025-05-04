



from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

import os
from pathlib import Path

def cargar_documento_y_guardar_en_chroma(ruta_pdf: str, persist_directory: str = "./chroma-data"):
    # Leer API key
    api_key = os.getenv("OPENAI_API_KEY") or Path("OpenAI_key.txt").read_text().strip()

    # 1. Cargar PDF
    loader = PyPDFLoader(ruta_pdf)
    documentos = loader.load()

    # 2. Trocear texto
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documentos)

    # 3. Embeddings
    embeddings = OpenAIEmbeddings(api_key=api_key)

    # 4. Persistencia local en el volumen compartido con Docker
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    print("✅ Documentos cargados y persistidos en Chroma (local)")




if __name__ == "__main__":
    # Asegúrate de que la ruta al PDF sea correcta
    cargar_documento_y_guardar_en_chroma("./data/ejemplo.pdf")  




















# from langchain_community.document_loaders import UnstructuredPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma

# from langchain_community.document_loaders import PyPDFLoader

# from chromadb.config import Settings


# api_key_path = "OpenAI_key.txt"

# try:
#     with open(api_key_path) as f:
#         api_key = f.read().strip()
# except FileNotFoundError:
#     print("No se encontró el archivo con la clave API.")




# def cargar_documento_y_guardar_en_chroma(ruta_pdf: str, persist_directory: str = "chroma-data"):
#     # 1. Cargar el documento

#     loader = PyPDFLoader(ruta_pdf)
#     documentos = loader.load()

#     # 2. Trocear el contenido
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunks = splitter.split_documents(documentos)

#     print(f"✅ Se han troceado {len(chunks)} documentos.")

#     # 3. Generar embeddings
#     embeddings = OpenAIEmbeddings(api_key=api_key)

#     print("✅ Se han generado los embeddings.")
#     print("embeddings", embeddings)

#     # 4. Guardar en Chroma
#     vectordb = Chroma.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         persist_directory=persist_directory,
#         client_settings=Settings(
#             chroma_api_impl="rest",
#             chroma_server_host="localhost",
#             chroma_server_http_port=8001
#         )
#     )

#     vectordb.persist()
#     print("✅ Documentos cargados y persistidos en Chroma")


# if __name__ == "__main__":
#     cargar_documento_y_guardar_en_chroma("./data/ejemplo.pdf")