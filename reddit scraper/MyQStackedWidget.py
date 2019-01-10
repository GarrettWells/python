from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import QObject


class MyQStackedWidget(QStackedWidget):

    def __init__(self, parent: QObject, obj: QStackedWidget):
        super().__init__(parent)
        if obj is None:
            self = QStackedWidget()
        else:
            self = obj

