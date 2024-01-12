# pip install PyQt6 pyqtgraph pyaudio

import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import pyqtgraph as pg
import pyaudio


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-time Spectrum Analyzer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.init_ui()

    def init_ui(self):
        self.graph_widget = pg.PlotWidget()
        self.layout.addWidget(self.graph_widget)

        # Set up PyAudio stream
        self.sample_rate = 44100
        self.chunk_size = 1024
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        # Initialize the frequency axis for the spectrum
        self.freq_axis = np.fft.fftfreq(self.chunk_size, d=1 / self.sample_rate)[
            : self.chunk_size // 2
        ]

        # Update the graph in a loop
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_spectrum)
        self.timer.start(50)  # Update every 50 milliseconds

        # Add start and stop buttons
        start_button = QPushButton("Start", self)
        stop_button = QPushButton("Stop", self)

        start_button.clicked.connect(self.start_audio_stream)
        stop_button.clicked.connect(self.stop_audio_stream)

        self.layout.addWidget(start_button)
        self.layout.addWidget(stop_button)

    def start_audio_stream(self):
        self.stream.start_stream()

    def stop_audio_stream(self):
        self.stream.stop_stream()

    def update_spectrum(self):
        # Read audio data from the stream
        raw_data = self.stream.read(self.chunk_size)
        audio_data = np.frombuffer(raw_data, dtype=np.int16)

        # Calculate spectrum using FFT
        spectrum = np.abs(np.fft.fft(audio_data)[: self.chunk_size // 2])

        # Update the graph
        self.graph_widget.plot(self.freq_axis, spectrum, clear=True, pen="g")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
