from slot import Slot
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class Picked(QWidget):
    def __init__(self, position: str):
        super().__init__()
        self.pos = position
        self.cur = 0
        self.setFixedSize(115 * 2 + 20, 115 * 6 + 20)
        self.setLayout(QGridLayout())
        self.layout().setDefaultPositioning(2, Qt.Horizontal)

        for _ in range(12):
            self.layout().addWidget(Slot())

    def pick(self, op: str):
        if self.pos == 'left':
            slot: Slot = self.layout().itemAtPosition(self.cur % 6, self.cur // 6).widget()
            slot.setPixmap(QPixmap(rf'img/{op}'))
            self.cur += 1
        else:
            if self.cur <= 5:
                slot: Slot = self.layout().itemAtPosition(self.cur, 1).widget()
            else:
                slot: Slot = self.layout().itemAtPosition(self.cur - 6, 0).widget()
            slot.setPixmap(QPixmap(rf'img/{op}'))
            self.cur += 1


class Banned(QWidget):
    def __init__(self, position):
        super().__init__()
        self.pos = position
        self.cur = 0
        self.slots = [Slot() for _ in range(5)]
        self.setLayout(QHBoxLayout())

        for slot in self.slots:
            self.layout().addWidget(slot)

    def ban(self, op: str):
        if self.pos == 'left':
            self.slots[self.cur].setPixmap(QPixmap(rf'img/{op}'))
            self.cur += 1
        else:
            self.slots[-self.cur - 1].setPixmap(QPixmap(rf'img/{op}'))
            self.cur += 1
