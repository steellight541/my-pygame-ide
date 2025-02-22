from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from .font_size import FontSizeLineEdit
from .theme import CustomThemeWindow

class SettingsLayout(QVBoxLayout):
    def __init__(self, parent: QMainWindow):
        super().__init__()
        # font size layout
        font_size_layout = QHBoxLayout()
        parent.font_size_label = QLabel("Font Size:")
        font_size_layout.addWidget(parent.font_size_label)
        parent.font_size_input = FontSizeLineEdit(parent)
        parent.font_size_input.setFixedWidth(50)
        parent.font_size_input.setText(str(parent.text_editor.textBlock.currentFont().pointSize()))
        font_size_layout.addWidget(parent.font_size_input)
        self.addLayout(font_size_layout)

        # theme layout
        theme_layout = QHBoxLayout()
        parent.theme_button = QPushButton("Customize Theme")
        parent.theme_button.clicked.connect(parent.open_theme_window)
        theme_layout.addWidget(parent.theme_button)
        self.addLayout(theme_layout)
        self.addStretch(1)

        # save button
        parent.save_button = QPushButton("Save")
        parent.save_button.clicked.connect(parent.save_settings)
        self.addWidget(parent.save_button)
        self.addStretch(1)
        