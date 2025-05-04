import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

class AudioRecorder:
    def __init__(self):
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        print("Grabando audio" )
        self.stream = self.audio.open(format=FORMAT,
                                       channels=CHANNELS,
                                       rate=RATE,
                                       input=True,
                                       frames_per_buffer=CHUNK)
        print("* Grabando...")

    def record(self):
        data = self.stream.read(CHUNK)
        self.frames.append(data)

    def stop_recording(self):
        print("\n* Grabación completada")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_audio(self, filename=WAVE_OUTPUT_FILENAME):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Audio guardado en {filename}")
        







# Configuración de grabación de audio
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# WAVE_OUTPUT_FILENAME = "output.wav"
# RECORD_SECONDS = 5
# MODEL_PATH = "models/small"
# MODEL_NAME = "small"

# def grabar_audio(segundos):
#     print(f"Grabando audio durante {segundos} segundos...")
    
#     audio = pyaudio.PyAudio()
#     stream = audio.open(format=FORMAT,
#                         channels=CHANNELS,
#                         rate=RATE,
#                         input=True,
#                         frames_per_buffer=CHUNK)
    
#     print("* Grabando...")
#     frames = []
    
#     for i in range(0, int(RATE / CHUNK * segundos)):
#         data = stream.read(CHUNK)
#         frames.append(data)
#         # Mostrar progreso
#         if i % 10 == 0:
#             sys.stdout.write(f"\rProgreso: {i/(RATE/CHUNK*segundos)*100:.1f}%")
#             sys.stdout.flush()
    
#     print("\n* Grabación completada")
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()
    
#     # Guardar archivo de audio
#     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(audio.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()
    
#     print(f"Audio guardado en {WAVE_OUTPUT_FILENAME}")
#     return WAVE_OUTPUT_FILENAME
