import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QPushButton, QWidget, QLabel, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from record_thread import RecorderThread
from whisper_thread import WhisperThread
from whisper_utils import cargar_modelo_whisper

RECORDING = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agente IA por Voz - Dark Mode")
        self.setMinimumSize(800, 600)
        
        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Título de la aplicación
        title_label = QLabel("Agente IA por Voz")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #E0E0E0;")
        layout.addWidget(title_label)
        
        # Área de texto para la transcripción
        self.transcription_area = QTextEdit()
        self.transcription_area.setPlaceholderText("La transcripción aparecerá aquí...")
        self.transcription_area.setReadOnly(True)
        layout.addWidget(self.transcription_area)
        
        # Botón de grabación
        self.record_button = QPushButton("Grabar Audio")
        self.record_button.setStyleSheet("background-color: #3D5AFE; color: white; padding: 10px;")
        self.record_button.clicked.connect(self.on_record_clicked)
        layout.addWidget(self.record_button)
        
        # Botón de envia transcripción
        self.send_button = QPushButton("Enviar Transcripción")
        self.send_button.setStyleSheet("background-color: #B0BEC5; color: white; padding: 10px;")
        self.send_button.setEnabled(False)
        layout.addWidget(self.send_button)
        
        # Estado
        self.status_label = QLabel("Listo")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: #E0E0E0;")
        layout.addWidget(self.status_label)
        
        self.recorder_thread = RecorderThread()
        self.modelo, self.device = cargar_modelo_whisper()
    
    def on_record_clicked(self):
        global RECORDING
        if not RECORDING:
            RECORDING = True
            print("RECORDING in if:", RECORDING)
            self.record_button.setEnabled(False)
            # Set button colors to indicate recording
            self.record_button.setStyleSheet("background-color: #FF4081; color: white; padding: 10px;")
            self.record_button.setText("Detener Grabación")
            self.status_label.setText("Grabando...")
            self.recorder_thread.recording_finished.connect(self.on_recording_finished)
            self.recorder_thread.start()
            self.record_button.setEnabled(True)
        else:
            print("RECORDING in else:", RECORDING)
            RECORDING = False
            self.record_button.setEnabled(False)
            self.status_label.setText("Deteniendo grabación...")
            # if hasattr(self, 'recorder_thread'):
            print("Deteniendo hilo de grabación")
            self.recorder_thread.stop()
            self.record_button.setText("Grabar Audio")
            self.record_button.setStyleSheet("background-color: #3D5AFE; color: white; padding: 10px;")
            self.status_label.setText("Transcribiendo...")

            
    def on_recording_finished(self, audio_data):
        self.status_label.setText("Grabación completada")
        self.record_button.setEnabled(True)
        
        self.transcription_area.clear()  # Limpiar el área de transcripción antes de mostrar el nuevo texto
        self.transcription_area.setPlainText("Transcribiendo...")
        self.status_label.setText("Transcribiendo...")
        # Actualizar el área de transcripción con el texto transcrito
        # transcription = transcribir_audio_bytes('output.wav', self.modelo, self.device)
        self.whisper_thread = WhisperThread('output.wav', self.modelo, self.device)
        self.whisper_thread.transcription_finished.connect(self.on_transcription_finished)
        self.whisper_thread.start()
        self.send_button.setEnabled(False)

    def on_transcription_finished(self, transcription):
        self.transcription_area.setPlainText(transcription)
        self.status_label.setText("Transcripción completada")
        self.send_button.setEnabled(True)
        # Set color to indicate ready state
        self.send_button.setStyleSheet("background-color: #3D5AFE; color: white; padding: 10px;")
        self.record_button.setEnabled(True)

def apply_dark_theme(app):
    """Aplica el tema oscuro a toda la aplicación"""
    app.setStyle("Fusion")
    
    # Configuración de la paleta oscura
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    # Estilo adicional para widgets específicos
    app.setStyleSheet("""
        QToolTip { color: #ffffff; background-color: #2a2a2a; border: 1px solid #767676; }
        QMenuBar::item:selected { background: #3A3A3A; }
        QListView::item:hover { background: #2A2A2A; }
        QTextEdit { border: 1px solid #555555; }
    """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())