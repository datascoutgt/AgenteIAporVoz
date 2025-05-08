
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel


from agente_sql import ejecutar_consulta_sql
from rag_query import ejecutar_consulta_rag
from rag_loader import cargar_documento_y_guardar_en_chroma
from triage import clasificar_intencion


from pathlib import Path
import shutil

app = FastAPI()


class Consulta(BaseModel):
    pregunta: str


@app.post("/consulta_sql")
def consultar_bd(data: Consulta):
    resultado = ejecutar_consulta_sql(data.pregunta)
    return {"respuesta": resultado}


@app.post("/consulta_rag")
def consultar_rag(data: Consulta):
    resultado = ejecutar_consulta_rag(data.pregunta)
    return {"respuesta": resultado}


# Crear el directorio "data" si no existe
UPLOAD_DIR = Path("data")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload-pdf")
async def subir_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")
    
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    cargar_documento_y_guardar_en_chroma(file_path)

    return {"mensaje": f"📄 Archivo '{file.filename}' guardado en {UPLOAD_DIR}/"}


@app.post("/triage")
def clasifica_intencion(data: Consulta):
    resultado = clasificar_intencion(pregunta=data.pregunta)
    if resultado == "sql":
        resultado = ejecutar_consulta_sql(data.pregunta)
        return {"respuesta": resultado}
    
    elif resultado == "rag":
        resultado = ejecutar_consulta_rag(data.pregunta)
        return {"respuesta": resultado}
    else:
        return {"respuesta": "saludo"}
