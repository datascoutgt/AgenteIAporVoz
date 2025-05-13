from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from typing import Optional

# --- Función principal para crear el agente y ejecutar una consulta ---
def ejecutar_consulta_sql(prompt_usuario: str, api_key_path: str = "OpenAI_key.txt") -> Optional[str]:
    """
    Ejecuta una consulta en lenguaje natural contra una base de datos PostgreSQL usando LangChain.

    Args:
        prompt_usuario (str): La consulta del usuario en lenguaje natural.
        api_key_path (str): Ruta al archivo de texto que contiene la clave API de OpenAI.

    Returns:
        str: Respuesta generada por el agente.
    """
    # Leer y limpiar la clave API
    try:
        with open(api_key_path) as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        return "No se encontró el archivo con la clave API."

    # Inicializar modelo de lenguaje con temperatura baja (determinismo)
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0)

    config = {
        'user': 'postgres',
        'password': 'pass',
        'host': '172.17.0.1',
        'port': '5433',
        'database': 'northwind'
    }

    # Cadena de conexión válida para SQLAlchemy
    connection_string = (f"postgresql+psycopg2://{config['user']}:{config['password']}"f"@{config['host']}:{config['port']}/{config['database']}")

    # Crear conexión a la base de datos
    try:
        db = SQLDatabase.from_uri(connection_string)
    except Exception as e:
        return f"Error conectando a la base de datos: {e}"

    # Crear agente SQL con LangChain
    try:
        agent = create_sql_agent(
            llm=llm,
            db=db,
            verbose=True
        )

        # Ejecutar la consulta
        respuesta = agent.invoke(prompt_usuario)
        return str(respuesta)

    except Exception as e:
        return f"Error ejecutando la consulta: {e}"
