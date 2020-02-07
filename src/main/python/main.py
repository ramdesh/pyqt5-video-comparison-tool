from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
import sys

from video_player.video_dialog import VideoDialog


class OriginalVideoDialog(VideoDialog):
    def __init__(self):
        super().__init__()
        self.title = 'Original Video'
        self.left = 500
        self.top = 10
        self.width = 640
        self.height = 480

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


class ProcessedVideoDialog(VideoDialog):
    def __init__(self):
        super().__init__()
        self.title = 'Processed Video'
        self.left = 1000
        self.top = 10
        self.width = 640
        self.height = 480

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


class AvanosUi(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Avanos Video Processor'
        self.left = 600
        self.top = 300
        self.width = 320
        self.height = 200
        self.original_video_dialog = OriginalVideoDialog()
        self.processed_video_dialog = ProcessedVideoDialog()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        submit_video_button = QPushButton('Submit Video', self)
        submit_video_button.setToolTip('Click here to select and submit a video')
        submit_video_button.move(100, 70)
        submit_video_button.clicked.connect(self.on_submit_video_button_clicked)

        self.show()

    def on_submit_video_button_clicked(self):
        self.open_file_name_dialog()

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a video file", "", "MP4 Files (*.mp4)", options=options)
        if file_name and file_name is not '':
            print('Opening ' + file_name)
            self.original_video_dialog.open_file_for_playing(file_name)
            self.original_video_dialog.show()

    def open_file_names_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "", "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(file_name)


if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    ex = AvanosUi()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
