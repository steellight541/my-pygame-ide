from styles import StyleSheet
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QColorDialog, QLineEdit, QLabel
from PyQt6.QtCore import Qt

class CustomThemeWindow(QDialog):
    style_sheet: StyleSheet = StyleSheet()
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Customize Theme")
        self.setGeometry(200, 200, 400, 300)
        self.setWindowModality(Qt.WindowModality.NonModal)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Background color button
        self.background_color_button = QPushButton("Background Color")
        self.background_color_button.clicked.connect(self.open_background_color_picker)
        layout.addWidget(self.background_color_button)

        # Text color button
        self.text_color_button = QPushButton("Text Color")
        self.text_color_button.clicked.connect(self.open_text_color_picker)
        layout.addWidget(self.text_color_button)

        # Font size input
        self.font_size_label = QLabel("Font Size:")
        layout.addWidget(self.font_size_label)
        self.font_size_input = QLineEdit()
        layout.addWidget(self.font_size_input)

        # Font family input
        self.font_family_label = QLabel("Font Family:")
        layout.addWidget(self.font_family_label)
        self.font_family_input = QLineEdit()
        layout.addWidget(self.font_family_input)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_custom_style)
        layout.addWidget(self.save_button)

        self.show()

    def open_background_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.style_sheet.set_background_color(color.name())

    def open_text_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.style_sheet.set_color(color.name())

    def save_custom_style(self):
        font_size = self.font_size_input.text()
        if font_size.isdigit():
            self.style_sheet.set_font_size(int(font_size))
        font_family = self.font_family_input.text()
        if font_family:
            self.style_sheet.set_font_family(font_family)
        self.parent.text_editor.set_style_sheet(self.style_sheet)
        self.accept()

