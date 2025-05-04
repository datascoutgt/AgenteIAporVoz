from PySide6.QtCore import QThread, Signal
from whisper_utils import transcribir_audio_bytes

class WhisperThread(QThread):
    transcription_finished = Signal(str)

    def __init__(self, audio_path, modelo, device):
        super().__init__()
        self.audio_path = audio_path
        self.modelo = modelo
        self.device = device

    def run(self):
        print("Transcribiendo audio...")
        transcription = transcribir_audio_bytes(self.audio_path, self.modelo, self.device)
        self.transcription_finished.emit(transcription)
        print("Transcripción completada")