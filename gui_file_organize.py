from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QPushButton, QVBoxLayout, QWidget, QFileDialog, QCheckBox
import os
import shutil
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))


def run():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


def organizer(path, apply_to_subfolders):
    if apply_to_subfolders:
        organize_file_all(path)
    else:
        organize_file(path)


def organize_file_all(directory):
    file_list = os.listdir(directory)

    for file in file_list:
        file_path = os.path.join(directory, file)

        if os.path.isfile(file_path):
            extension = file[file.rfind(".") + 1:]
            subdirectory = os.path.join(directory, extension)
            try:
                os.makedirs(subdirectory)

            except FileExistsError:
                pass

            shutil.move(file_path, os.path.join(subdirectory, file))

        elif os.path.isdir(file_path):
            organize_file_all(file_path)


def organize_file(directory):
    file_list = os.listdir(directory)

    for file in file_list:
        file_path = os.path.join(directory, file)

        if os.path.isfile(file_path):
            extension = file[file.rfind(".") + 1:]
            subdirectory = os.path.join(directory, extension)
            try:
                os.makedirs(subdirectory)

            except FileExistsError:
                pass

            shutil.move(file_path, os.path.join(subdirectory, file))


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        screen_info = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen_info.width(), screen_info.height()

        x_center = (screen_width - 800) // 2
        y_center = (screen_height - 600) // 2

        self.setGeometry(x_center, y_center, 800, 600)

        self.web_viewer = QWebEngineView()
        self.web_viewer.setUrl(QUrl.fromLocalFile(os.path.join(current_dir, "gui", "index.html")))

        # Add a checkbox
        self.checkbox = QCheckBox("Apply to subfolders")

        # Set a style to increase the font size
        style = "font-size: 26px;"  # You can adjust the size according to your needs
        self.setStyleSheet(style)

        # Add a button to select a folder
        select_folder_button = QPushButton('Select Folder')
        select_folder_button.clicked.connect(self.select_folder)

        # Vertical layout to organize the elements
        vertical_layout = QVBoxLayout()

        vertical_layout.addWidget(self.checkbox)
        vertical_layout.addWidget(select_folder_button)

        # Widget container for the layout
        widget_container = QWidget()
        widget_container.setLayout(vertical_layout)

        self.setCentralWidget(widget_container)

    def select_folder(self):
        # Show the directory selection dialog
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder', '/')
        if folder_path:
            # Only call organizer if a folder is selected
            organizer(folder_path, self.checkbox.isChecked())


if __name__ == "__main__":
    run()

