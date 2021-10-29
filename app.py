import sys

from PyQt5.QtWidgets import QApplication

from interface import Window
from process import Identify
from client import Client


class App:
    def __init__(self):
        super().__init__()
        self.qapp = QApplication(sys.argv)
        self.win = Window(self)
        self.win.show()
        self.identify = Identify(self.win)
        self.client = Client(self)

    def run(self):

        self.client.start()
        sys.exit(self.qapp.exec_())


if __name__ == '__main__':
    app = App()
    app.run()
