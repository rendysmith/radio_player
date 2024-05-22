import sys
import vlc
import mutagen
from mutagen.mp3 import MP3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QLineEdit, QLabel
from PyQt5.QtCore import Qt

class RadioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Internet Radio Player')
        self.setGeometry(100, 100, 300, 200)

        # VLC player instance
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Layout
        layout = QVBoxLayout()

        # Stream URL input
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Enter stream URL')
        layout.addWidget(self.url_input)

        # Track title
        self.track_label = QLabel('Track Title', self)
        layout.addWidget(self.track_label)

        # Play button
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.play_stream)
        layout.addWidget(self.play_button)

        # Stop button
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_stream)
        layout.addWidget(self.stop_button)

        # Volume control
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)

        self.setLayout(layout)

    def play_stream(self):
        url = self.url_input.text()
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()
        metadata = self.get_stream_metadata(url)
        self.track_label.setText(metadata)

    def stop_stream(self):
        self.player.stop()
        self.track_label.setText('Stopped')

    def set_volume(self, value):
        self.player.audio_set_volume(value)

    def get_stream_metadata(self, url):
        try:
            audio = MP3(url)
            artist = audio.get('artist', ['Unknown'])[0]
            title = audio.get('title', ['Unknown'])[0]
            return f"{artist} - {title}"
        except mutagen.MutagenError:
            return "No metadata available"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = RadioPlayer()
    player.show()
    sys.exit(app.exec_())