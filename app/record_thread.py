from PySide6.QtCore import QThread, Signal
from audio_utils import AudioRecorder
import time

class RecorderThread(QThread):
    recording_finished = Signal(bytes)

    def __init__(self):
        super().__init__()
        self._running = True
        self.recorder = AudioRecorder()

    def run(self):
        self.recorder.start_recording()
  
        while self._running:
            self.recorder.record()
            time.sleep(0.01)  # Evita sobrecargar la CPU
        self.recorder.stop_recording()
        audio_data = self.recorder.save_audio()
        self.recording_finished.emit(audio_data)
        

    def stop(self):
        self._running = False
