import os
from threading import Event
from typing import Optional
from PySide6.QtWidgets import (QPushButton, QGridLayout, QWidget,
                               QTabWidget, QScrollArea)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize


class ConfirmButton(QPushButton):
    def __init__(self):
        super().__init__('Loading...')
        self.setEnabled(False)
        self.payload = []
        self.t_event: Optional[Event] = None
        self.stage: Optional[Operator] = None
        self.setFixedHeight(80)
        self.clicked.connect(self.confirm)

    def confirm(self):
        if self.stage.image:
            self.payload[0] = self.stage.image
            self.setEnabled(False)
            self.t_event.set()


class Operator(QPushButton):
    def __init__(self, image: str):
        super().__init__()
        self.confirm: Optional[ConfirmButton] = None
        self.image = image
        self.setFixedSize(130, 130)
        self.setIcon(QPixmap(rf'img/{self.image}'))
        self.setIconSize(QSize(120, 120))
        self.setCheckable(True)
        self.clicked.connect(self.select)

    def select(self):
        if self.confirm.stage:
            self.confirm.stage.setChecked(False)
        self.confirm.stage = self


class Pool(QTabWidget):
    def __init__(self, confirm: ConfirmButton):
        super().__init__()
        self.setTabPosition(QTabWidget.East)
        self.all = {}
        classes = ('guard', 'sniper', 'caster', 'defender',
                   'specialist', 'supporter', 'medic', 'vanguard')
        for op_class in classes:
            page = QScrollArea()
            grid = QWidget()
            grid.setLayout(QGridLayout())
            grid.layout().setDefaultPositioning(4, Qt.Vertical)

            ops = os.listdir(rf'img/{op_class}')
            ops.remove('no_select.png')
            for op in ops:
                op_button = Operator(rf'{op_class}/{op}')
                op_button.confirm = confirm
                self.all[f'{op_class}/{op}'] = op_button
                grid.layout().addWidget(op_button)
            no_sel_button = Operator(rf'{op_class}/no_select.png')
            no_sel_button.confirm = confirm
            grid.layout().addWidget(no_sel_button)

            page.setWidget(grid)
            self.addTab(page, QIcon(rf'img/class_icons/{op_class}.png'), '')
            self.setIconSize(QSize(45, 45))
