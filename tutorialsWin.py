import time
from threading import Event, Thread
import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QDir, pyqtSignal, QObject
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QDialog
from os import listdir

from process import Identify
from tutorialsWindow import Ui_Dialog


class TutorialsWin(Ui_Dialog, QDialog):
    def __init__(self):
        super(TutorialsWin, self).__init__()
        # self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.gestures = []
        self.currentGes = ''
        self.gridLayout.removeWidget(self.lbl_change)
        self.lbl_change.close()
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist(self.player)
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        self.vw = QVideoWidget()
        self.player.setVideoOutput(self.vw)
        self.player.setPlaylist(self.playlist)
        self.playlist.setMediaObject(self.player)
        self.gridLayout.addWidget(self.vw, 0, 0, 1, 2)
        self.btn_last.clicked.connect(self.last)
        self.btn_next.clicked.connect(self.next)
        self.timer = Timer()
        self.timer.count1s.connect(self._next_sec)
        self.timer.timeout.connect(self.next)
        self.identify = Identify(self)
        self.eventRunning = Event()
        self.eventRunning.set()
        self.identify.start()
        self.show()
        self.init_list()

    def init_list(self):
        for file in listdir('videos'):
            name = file.split('.')[0]
            url = QUrl.fromLocalFile(QDir.currentPath() + '/videos/' + file)
            self.playlist.addMedia(QMediaContent(url))
            self.gestures.append(name)
        # print(self.playlist.currentIndex())
        self.next()

    def last(self):
        self._set_current_index(self.playlist.currentIndex() - 1)

    def next(self):
        self._set_current_index(self.playlist.currentIndex() + 1)

    def _set_current_index(self, target_index):
        # print(self.playlist.currentIndex(), target_index)
        self.btn_next.setText("下一个 >>")
        if 0 <= target_index < len(self.gestures):
            self.player.pause()
            self.playlist.setCurrentIndex(target_index)
            self.player.play()
            self.currentGes = self.gestures[target_index]
        self._set_labels(False)
        print(self.playlist.currentIndex())
        self.btn_last.setEnabled(self.playlist.currentIndex() > 0)
        self.btn_next.setEnabled(self.playlist.currentIndex() < len(self.gestures)-1)

    def set_gesture(self, gesture: str):
        print("做出手势:"+gesture, "目前手势:"+self.currentGes)
        if gesture != '' and gesture == self.currentGes:
            self._set_labels(True)
            self.auto_next()

    def _set_labels(self, is_bingo: bool):
        self.lbl_msg.setText(
            "恭喜你，做出了正确的{}手势！".format(self.currentGes) if is_bingo else '请模仿左侧视频做出{}手势'.format(self.currentGes))
        self.lbl_gesture.setStyleSheet('color: rgb(0, 255, 127);' if is_bingo else '')
        self.lbl_gesture.setText(self.currentGes)

    def flash_img(self, image, ratio):
        size = (int(self.lbl_img.width()), int(self.lbl_img.width() * ratio))
        shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(shrink.data, shrink.shape[1],
                           shrink.shape[0], shrink.shape[1] * 3,
                           QtGui.QImage.Format_RGB888)
        self.lbl_img.setPixmap(QtGui.QPixmap.fromImage(img))

    def auto_next(self):
        self.timer.start()

    def _next_sec(self, count: int):
        self.btn_next.setText("下一个({}) >>".format(str(count)))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.identify.break_loop()
        self.eventRunning.clear()
        self.player.stop()


class Timer(QObject):
    count1s = pyqtSignal(int)
    timeout = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._count = 3

    def start(self):
        Thread(target=self.run).start()

    def run(self):
        while self._count > 0:
            self.count1s.emit(self._count)
            self._count -= 1
            time.sleep(1)
        self.timeout.emit()
        self._count = 3
