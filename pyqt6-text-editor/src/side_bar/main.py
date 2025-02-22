from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QTreeWidgetItem, QLabel, QWidget, QVBoxLayout, QMainWindow, QSplitter
from PyQt6.QtGui import QIcon
import os
from .widgets import SideBarTree, PopulateSidebarThread

class SideBar(QWidget):
    def __init__(self, parent: QSplitter, root_directory):
        super().__init__()
        self.this_thread = None
        self.parent: QMainWindow = parent # MainWindow instance
        self.root_directory = root_directory

        self.layout = QVBoxLayout() # Vertical layout

        # Label
        self.label = QLabel("Folder Structure")
        self.layout.addWidget(self.label)

        # Tree widget
        self.tree = SideBarTree(self)
        self.layout.addWidget(self.tree)

        # initial population of the sidebar
        self.set_root_directory(root_directory)
        self.setLayout(self.layout)

    def on_thread_finished(self, directory):
        self.this_thread = None
        self.populate_sidebar(directory)

    def closeEvent(self, a0):
        if self.this_thread is not None and self.this_thread.isRunning():
            self.this_thread.quit()
            self.this_thread.wait()
        a0.accept()
            
    def populate_sidebar(self, directory):
        self.tree.clear()
        self.add_items(self.tree.invisibleRootItem(), directory)

    def add_items(self, parent, directory):
        for item in os.listdir(directory):
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                folder_item = QTreeWidgetItem(parent, [item])
                folder_item.setIcon(0, QIcon("folder_icon.png"))
                folder_item.setData(0, Qt.ItemDataRole.UserRole, path)
                self.add_items(folder_item, path)
            else:
                file_item = QTreeWidgetItem(parent, [item])
                file_item.setIcon(0, QIcon("file_icon.png"))
                file_item.setData(0, Qt.ItemDataRole.UserRole, path)

    def on_item_double_clicked(self, item):
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and os.path.isfile(file_path): self.parent.text_editor.open_file(file_path)
    
    def open_folder_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.set_root_directory(directory)
            
    def refresh(self):
        if self.this_thread is None:
            self.this_thread = PopulateSidebarThread(self, self.root_directory)
            self.this_thread.finished.connect(lambda directory: self.on_thread_finished(directory))
            self.this_thread.start()

    def set_root_directory(self, directory):
        self.root_directory = directory
        self.refresh()

