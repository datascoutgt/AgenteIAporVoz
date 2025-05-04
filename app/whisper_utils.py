# Read the output.wav file and print the text with Whisper small model
import whisper
import torch
from pathlib import Path
import librosa
import io

# # Configuración de grabación de audio
WAVE_OUTPUT_FILENAME = "output.wav"
MODEL_PATH = "models/small"
MODEL_NAME = "small"


def cargar_modelo_whisper():
    print(f"Cargando modelo Whisper '{MODEL_NAME}'...")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando dispositivo: {device}")
    
    # Verificar si el modelo existe localmente usando pathlib.Path
    model_dir = Path(MODEL_PATH)
    modelo_local_path = model_dir / "small.pt"
    
    if modelo_local_path.exists():
        print(f"Cargando modelo local desde {modelo_local_path}")
        modelo = whisper.load_model(MODEL_NAME, device=device, download_root=str(model_dir))
    else:
        print(f"Modelo no encontrado en {modelo_local_path}, descargando...")
        # Crear el directorio si no existe
        model_dir.mkdir(parents=True, exist_ok=True)
        modelo = whisper.load_model(MODEL_NAME, device=device, download_root=str(model_dir))
        print(f"Modelo descargado en {model_dir}")
    
    print("Modelo cargado correctamente")
    return modelo, device

def transcribir_audio_bytes(audio_path, modelo, device):
    print("Transcribiendo audio desde memoria...")

    # Leer los bytes del archivo
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    # Cargar el audio desde bytes a un array numpy
    audio_buffer = io.BytesIO(audio_bytes)
    
    # Cargar el audio en formato numpy (librosa espera una tasa de muestreo de 16kHz)
    y, sr = librosa.load(audio_buffer, sr=16000, mono=True) # Whisper espera 16 kHz
    
    # Transcribir el audio usando el modelo Whisper
    # Usamos `fp16=True` para acelerar el proceso si estamos en CUDA
    result = modelo.transcribe(y, fp16=True if device == "cuda" else False)

    return result["text"]