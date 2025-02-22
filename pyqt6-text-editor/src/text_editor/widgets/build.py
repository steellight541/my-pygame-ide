from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QWidget
from PyQt6.QtCore import QProcess, pyqtSignal
import codecs

class BuildOutput(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Build Output")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout(self)
        self.textBlock = QTextEdit()
        layout.addWidget(self.textBlock)
        self.textBlock.setReadOnly(True)
        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        layout.addWidget(self.closeButton)

    def append_text(self, text: str):
        self.textBlock.append(text)

class BuildProcess(QProcess):
    output = pyqtSignal(str)
    def __init__(self, parent: QWidget, file_path: str):
        super().__init__(parent)
        self.file_path = file_path
        self.decoder = codecs.getincrementaldecoder('utf-8')()
        self.readyReadStandardOutput.connect(self.on_ready_read_standard_output)
        self.readyReadStandardError.connect(self.on_ready_read_standard_error)
        self.finished.connect(self.on_finished)

    def on_ready_read_standard_output(self):
        data = self.readAllStandardOutput().data()
        text = self.decoder.decode(data)
        self.output.emit(text)

    def on_ready_read_standard_error(self):
        data = self.readAllStandardError().data()
        text = self.decoder.decode(data)
        self.output.emit(text)

    def on_finished(self):
        remaining_text = self.decoder.decode(b'', final=True)
        if remaining_text: self.output.emit(remaining_text)
