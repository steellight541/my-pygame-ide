from .widgets import SettingsLayout
from PyQt6.QtWidgets import QDialog, QMainWindow
from PyQt6.QtCore import Qt
from .widgets import CustomThemeWindow

class SettingsWindow(QDialog):
    def __init__(self, parent: QMainWindow):
        super().__init__()

        self.parent = parent

        self.setWindowTitle("Settings")
        self.setGeometry(150, 150, 400, 300)
        self.setWindowModality(Qt.WindowModality.NonModal)  # Set to non-modal

        layout = SettingsLayout(self.parent)
        self.setLayout(layout)


        self.show()

    def open_theme_window(self):
        self.theme_window = CustomThemeWindow(self.parent)
        self.theme_window.show()

    def save_settings(self):
        self.parent.text_editor.update_font_size()
        self.close()



    def open_theme_window(self):
        self.theme_window = CustomThemeWindow(self.parent)
        self.theme_window.show()

    def save_settings(self):
        self.parent.text_editor.update_font_size()
        self.close()