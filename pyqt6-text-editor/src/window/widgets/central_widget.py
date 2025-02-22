from PyQt6.QtWidgets import QSplitter
from PyQt6.QtCore import Qt
from side_bar import SideBar
from text_editor import TextEditor
import os

class CentralWidget(QSplitter):
    def __init__(self, parent):
        super().__init__(Qt.Orientation.Horizontal, parent)
        parent.text_editor = TextEditor(parent)
        parent.side_bar = SideBar(parent, os.getcwd())
        self.addWidget(parent.side_bar)
        self.addWidget(parent.text_editor)
        self.setSizes([200, 600])