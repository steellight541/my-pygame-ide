from PyQt6.QtWidgets import QLineEdit
class FontSizeLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent


    def wheelEvent(self, a0):
        current_size = int(self.text()) if self.text().isdigit() else 0
        delta = a0.angleDelta().y() // 120
        new_size = max(1, current_size + delta)
        self.setText(str(new_size))
        self.parent.text_editor.set_font_size(new_size)

