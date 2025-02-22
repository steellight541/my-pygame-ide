from PyQt6.QtCore import QThread, pyqtSignal

class PopulateSidebarThread(QThread):
    finished = pyqtSignal(object)
    def __init__(self, parent, directory):
        super().__init__()
        self.parent = parent
        self.directory = directory

    def run(self):
        self.finished.emit(self.directory)