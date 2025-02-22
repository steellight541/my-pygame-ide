from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QFileDialog, QMainWindow, QDialog, QPushButton
from PyQt6.QtGui import QFont
from styles import StyleSheet
from syntax_highlighter import SyntaxHighlighter
import pathlib
import subprocess
from .widgets import BuildOutput, BuildProcess




class TextEditor(QWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__()
        self.styles = {
            "dark": StyleSheet.dark(),
            "light": StyleSheet.light(),
            "custom": StyleSheet.dark()
        }

        self.parent = parent

        self.current_style = StyleSheet()
        layout = QVBoxLayout(self)
        self.textBlock = QTextEdit()
        layout.addWidget(self.textBlock)
        self.highlighter = SyntaxHighlighter(self.textBlock.document(), "txt")

        self.setGeometry(100, 100, 800, 600)

    def open_file_dialog(self):
        options = QFileDialog.Option.DontConfirmOverwrite
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name: self.open_file(file_name)

    def open_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file: self.textBlock.setPlainText(file.read())
        self.current_file_path = file_path
        file_extension = file_path.split('.')[-1]
        self.highlighter = SyntaxHighlighter(self.textBlock.document(), "." + file_extension)
        self.current_file_path = pathlib.Path(file_path).as_posix()

    def save_file_dialog(self):
        if hasattr(self, 'current_file_path') and self.current_file_path:
            self.save_file(self.current_file_path)
        else:
            self.save_as_file_dialog()

    def save_as_file_dialog(self):
        options = QFileDialog.Option.DontConfirmOverwrite | QFileDialog.Option.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*);;Text Files (*.txt);;Python Files (*.py)", options=options)
        if file_name: self.save_file(file_name)

    def save_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.textBlock.toPlainText())
        self.current_file_path = pathlib.Path(file_path).as_posix()

    def set_style_sheet(self, style_sheet: StyleSheet):
        self.textBlock.setStyleSheet(str(style_sheet))

    def set_font_size(self, font_size):
        self.font_size = font_size
        self.textBlock.setFont(QFont(self.textBlock.font().family(), self.font_size))

    def run_file(self):
        if hasattr(self, 'current_file_path') and self.current_file_path:
            if self.current_file_path.endswith('.py'):
                subprocess.run(['python', self.current_file_path])
            else:
                print("File is not a python file")

    def build_file(self):
        if hasattr(self, 'current_file_path') and self.current_file_path:
            if self.current_file_path.endswith('.py'):
                # check if already building
                self.build_output = BuildOutput(self)
                self.build_output.show()
                self.build_output.append_text("Building file...")
                build_path = TextEditor.build_path(self.current_file_path, "/build")
                self.build_process = BuildProcess(self.build_output, self.current_file_path)
                self.build_process.output.connect(self.build_output.append_text)
                # pyinstaller --onefile --windowed
                self.build_process.start("pyinstaller", [
                    "--onefile",
                    "--windowed",
                    self.current_file_path,
                    f"--distpath={build_path}/dist",
                    f"--workpath={build_path}/build",
                    f"--specpath={build_path}/spec"
                ])
                self.build_process.finished.connect(self.on_build_finished)
            else:
                print("File is not a python file")

    def on_build_finished(self):
        returncode = self.build_process.exitCode()
        if returncode == 0:
            self.build_output.append_text("Build complete you can close down this window")
            self.parent.side_bar.refresh()
        else: self.build_output.append_text("Build failed")
        self.build_process.close()


    @staticmethod
    def build_path(file_path, output_folder) -> str:
        return "/".join(file_path.split("/")[0:-2 if TextEditor.last_folder(TextEditor.folder_path(file_path)).endswith("src") else -1]) + output_folder

    @staticmethod
    def folder_path(file_path) -> str:
        return "/".join(file_path.split("/")[:-1])

    @staticmethod
    def last_folder(file_path) -> str:
        return file_path.split("/")[-1]