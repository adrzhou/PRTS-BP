from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap


class Slot(QLabel):
    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
        self.setFixedSize(115, 115)
        self.setPixmap(QPixmap(r'img/empty.png'))
