from PyQt5.QtWidgets import QDialog

from helpWindow import Ui_Dialog


class HelpWin(Ui_Dialog, QDialog):
    def __init__(self):
        super(HelpWin, self).__init__()
        self.setupUi(self)
        self.show()