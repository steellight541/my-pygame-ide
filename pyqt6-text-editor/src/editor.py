from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QFileDialog, QMenuBar
from PyQt6.QtGui import QAction, QFont
from syntax_highlighter import SyntaxHighlighter
from styles import StyleSheet
import os

class TextEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.font_size = 12
        self.style_sheet = StyleSheet.dark()
        layout = QVBoxLayout(self)
        self.editor = QTextEdit()
        layout.addWidget(self.editor)

        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)

        self.create_actions()
        self.create_menus()
        self.apply_style_sheet()
        self.highlighter = SyntaxHighlighter(self.editor.document(), "txt")

    def create_actions(self):
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_file_dialog)

        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save_file_dialog)

    def create_menus(self):
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        layout = self.layout()
        layout.setMenuBar(menu_bar)

    def open_file_dialog(self):
        options = QFileDialog.Option.DontConfirmOverwrite
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            self.open_file(file_name)

    def save_file_dialog(self):
        options = QFileDialog.Option.DontConfirmOverwrite
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name: self.save_file(file_name)

    def open_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file: self.editor.setPlainText(file.read())
        file_extension = os.path.splitext(file_path)[1]
        self.highlighter = SyntaxHighlighter(self.editor.document(), file_extension)

    def save_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file: file.write(self.editor.toPlainText())

    def toggle_dark_mode(self):
        editor_style = self.editor.styleSheet()
        if "background-color: black" in editor_style: self.editor.setStyleSheet("background-color: white; color: black;")
        else: self.editor.setStyleSheet("background-color: black; color: white;")

    def set_font_size(self, font_size):
        self.font_size = font_size
        cursor = self.editor.textCursor()
        position = cursor.position()
        self.editor.selectAll()
        self.editor.setFontPointSize(self.font_size)
        cursor.setPosition(position)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    def set_style_sheet(self, style_sheet: StyleSheet):
        self.style_sheet = style_sheet
        self.apply_style_sheet()

    def apply_style_sheet(self):
        self.editor.setStyleSheet(str(self.style_sheet))
        if self.style_sheet.font_size:
            self.set_font_size(self.style_sheet.font_size)
        if self.style_sheet.font_family:
            self.editor.setFont(QFont(self.style_sheet.font_family, self.style_sheet.font_size or self.font_size))
