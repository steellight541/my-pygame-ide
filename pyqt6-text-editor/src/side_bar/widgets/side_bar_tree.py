from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QInputDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import os, shutil

class SideBarTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setMouseTracking(True)
        self.setHeaderHidden(True)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)

    def on_item_double_clicked(self, item):
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and os.path.isfile(file_path): self.parent.parent.text_editor.open_file(file_path)

    # right click menu
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        # pressed item
        self.pressedItem = self.itemAt(event.pos())

        refresh_action = menu.addAction("Refresh")
        refresh_action.triggered.connect(self.on_refresh_triggered)

        add_folder_action = menu.addAction("Add Folder")
        add_folder_action.triggered.connect(self.add_folder)

        add_file_action = menu.addAction("Add File")
        add_file_action.triggered.connect(self.add_file)

        rename_action = menu.addAction("Rename")
        rename_action.triggered.connect(self.rename)

        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.on_delete)


        menu.exec(event.globalPos())


    def on_delete(self):
        # delete the pressed item
        if self.pressedItem is not None:
            item_path = self.pressedItem.data(0, Qt.ItemDataRole.UserRole)
            # check if file or folder
            if os.path.isdir(item_path): shutil.rmtree(item_path)
            else: os.remove(item_path)
            self.pressedItem.parent().removeChild(self.pressedItem)
        
    def add_folder(self):
        # append a folder on the pressed item
        folder_name, ok = QInputDialog.getText(self, "Folder Name", "Enter folder name:")
        if ok and folder_name:
            folder = QTreeWidgetItem(self.pressedItem, [folder_name])
            os.makedirs(os.path.join(self.pressedItem.data(0, Qt.ItemDataRole.UserRole), folder_name))
            folder.setIcon(0, QIcon("folder_icon.png"))
            # set data
            folder.setData(0, Qt.ItemDataRole.UserRole, os.path.join(self.pressedItem.data(0, Qt.ItemDataRole.UserRole), folder_name))

    def add_file(self):
        # append a file on the pressed item
        file_name, ok = QInputDialog.getText(self, "File Name", "Enter file name:")
        if ok and file_name:
            file = QTreeWidgetItem(self.pressedItem, [file_name])
            open(os.path.join(self.pressedItem.data(0, Qt.ItemDataRole.UserRole), file_name), "w").close()
            file.setIcon(0, QIcon("file_icon.png"))
            # set data
            file.setData(0, Qt.ItemDataRole.UserRole, os.path.join(self.pressedItem.data(0, Qt.ItemDataRole.UserRole), file_name))

    def rename(self):
        # rename the pressed item
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:")
        if ok and new_name:
            self.pressedItem.setText(0, new_name)
            os.rename(self.pressedItem.data(0, Qt.ItemDataRole.UserRole), os.path.join(os.path.dirname(self.pressedItem.data(0, Qt.ItemDataRole.UserRole)), new_name))
            self.pressedItem.setData(0, Qt.ItemDataRole.UserRole, os.path.join(os.path.dirname(self.pressedItem.data(0, Qt.ItemDataRole.UserRole)), new_name))

    def on_refresh_triggered(self):
        if self.parent.this_thread is not None and self.parent.this_thread.isRunning():
            self.parent.this_thread.quit()
            self.parent.this_thread.wait()
        self.parent.refresh()
