from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget


class NativeVideoDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        video_widget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.set_position)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Maximum)

        # Create exit action
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Close window')
        exit_action.triggered.connect(self.exit_call)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.playButton)
        control_layout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        layout.addLayout(control_layout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(video_widget)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.error.connect(self.handle_error)

    def open_file_for_playing(self, file_name):
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(file_name)))
        self.playButton.setEnabled(True)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def media_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.positionSlider.setValue(position)

    def duration_changed(self, duration):
        self.positionSlider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_error(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def exit_call(self):
        self.close()