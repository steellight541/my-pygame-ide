from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtGui import QShortcut
from settings import SettingsWindow
from window.widgets import CentralWidget, MainWindowToolBar
from settings import SettingsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Pygame IDE")
        self.setMinimumSize(800, 600)

        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self.settings_window = None
        self.addToolBar(MainWindowToolBar(self))
        self.create_shortcuts()

    def open_theme_window(self):
        if not self.settings_window: self.settings_window = SettingsWindow(self)
        self.settings_window.open_theme_window()

    def save_settings(self):
        if not self.settings_window: self.settings_window = SettingsWindow(self)
        self.settings_window.save_settings()

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.side_bar.set_root_directory(folder)

    def save_file(self):
        self.text_editor.save_file(self.text_editor.current_file_path)

    def open_settings(self):
        if not self.settings_window: self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def create_shortcuts(self):
        save_shortcut = QShortcut("Ctrl+S", self)
        save_shortcut.activated.connect(self.save_file)

        open_shortcut = QShortcut("Ctrl+O", self)
        open_shortcut.activated.connect(self.text_editor.open_file_dialog)

        save_as_shortcut = QShortcut("Ctrl+Shift+S", self)
        save_as_shortcut.activated.connect(self.text_editor.save_as_file_dialog)

    def update_font_size(self):
        self.text_editor.update_font_size()
