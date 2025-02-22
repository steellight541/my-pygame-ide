from PyQt6.QtWidgets import QMainWindow, QToolBar, QToolButton, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

class MainWindowToolBar(QToolBar):
    def __init__(self, parent:QMainWindow):
        super().__init__()
        self.parent = parent

        file_button = QToolButton(self)
        file_button.setText("File")
        file_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        file_menu = QMenu(file_button)

        open_action = QAction("Open File", self)
        open_action.triggered.connect(parent.text_editor.open_file_dialog)
        file_menu.addAction(open_action)

        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(parent.open_folder)
        file_menu.addAction(open_folder_action)


        save_action = QAction("Save", self)
        save_action.triggered.connect(parent.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(parent.text_editor.save_as_file_dialog)
        file_menu.addAction(save_as_action)

        file_button.setMenu(file_menu)
        file_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addWidget(file_button)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(parent.open_settings)
        self.addAction(settings_action)

        build = QToolButton(self)
        build.setText("Build")
        build.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        build_menu = QMenu(build)

        run_action = QAction("Run", self)
        run_action.triggered.connect(parent.text_editor.run_file)
        build_menu.addAction(run_action)

        build_action = QAction("Build", self)
        build_action.triggered.connect(parent.text_editor.build_file)
        build_menu.addAction(build_action)

        build.setMenu(build_menu)
        build.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addWidget(build)

        self.addSeparator()