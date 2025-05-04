from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from pathlib import Path

def clasificar_intencion(pregunta: str) -> str:
    """
    Clasifica la intención de la pregunta del usuario como:
    - 'sql' para consultas a base de datos
    - 'rag' para recuperación desde documentos
    - 'saludo' para saludos o conversaciones triviales
    - 'otro' para cualquier otra cosa

    Returns:
        str: Una de las categorías anteriores
    """
    api_key = os.getenv("OPENAI_API_KEY") or Path("OpenAI_key.txt").read_text().strip()
    llm = ChatOpenAI(temperature=0, openai_api_key=api_key)

    prompt = PromptTemplate(
        input_variables=["pregunta"],
        template="""
        Clasifica la intención de esta pregunta: "{pregunta}"

        Elige solo una de estas opciones y responde solo con esa palabra:
        - sql: si se refiere a datos estructurados como empleados, pedidos, productos, ventas, etc.
        - rag: si parece buscar información detallada, explicaciones o contenido de documentos.
        - saludo: si es un saludo o pregunta trivial.
        - otro: si no encaja en ninguna de las anteriores.
        """
    )

    cadena = prompt.format(pregunta=pregunta)

    respuesta = llm.invoke(cadena).content.strip().lower()
    print(respuesta)
    # Normalizar por si responde con más de una palabra
    if "sql" in respuesta:
        return "sql"
    elif "rag" in respuesta:
        return "rag"
    elif "saludo" in respuesta:
        return "saludo"
    else:
        return "otro"


if __name__ == "__main__":
    pregunta = "¿Cuántos pedidos se hicieron en marzo?"
    pregunta = "dime cual es la principal causa de muerte materna en el mundo"
    pregunta = "¿cuantos tipos de pajaros hay en colombia?"
    destino = clasificar_intencion(pregunta)
    print(f"📌 Intención detectada: {destino}")