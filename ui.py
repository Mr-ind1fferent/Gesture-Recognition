# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1222, 715)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.window = QtWidgets.QWidget(self.centralwidget)
        self.window.setStyleSheet("QWidget#window{\n"
"        background:white;\n"
"        border-radius:10px;\n"
"\n"
"}")
        self.window.setObjectName("window")
        self.gridLayout = QtWidgets.QGridLayout(self.window)
        self.gridLayout.setContentsMargins(-1, -1, -1, 1)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 1, 1, 2)
        self.btn_get_ctrl = QtWidgets.QPushButton(self.window)
        self.btn_get_ctrl.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(85, 170, 255);\n"
"\n"
"padding:10px;\n"
"\n"
"border-radius:10px\n"
"")
        self.btn_get_ctrl.setObjectName("btn_get_ctrl")
        self.gridLayout.addWidget(self.btn_get_ctrl, 8, 1, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.window)
        self.textBrowser.setStyleSheet("QTextBrowser{\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"selection-background-color: darkgray;\n"
"border-color: rgb(85, 170, 255);\n"
"}")
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 13, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.window)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 2)
        self.btn_pause = QtWidgets.QPushButton(self.window)
        self.btn_pause.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(85, 170, 255);\n"
"\n"
"padding:10px;\n"
"\n"
"border-radius:10px\n"
"")
        self.btn_pause.setObjectName("btn_pause")
        self.gridLayout.addWidget(self.btn_pause, 8, 2, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self.window)
        self.btn_start.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(85, 170, 255);\n"
"\n"
"padding:10px;\n"
"\n"
"border-radius:10px\n"
"")
        self.btn_start.setObjectName("btn_start")
        self.gridLayout.addWidget(self.btn_start, 7, 1, 1, 2)
        self.checkBox = QtWidgets.QCheckBox(self.window)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 12, 1, 1, 2)
        self.btn_join = QtWidgets.QPushButton(self.window)
        self.btn_join.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(85, 170, 255);\n"
"\n"
"padding:10px;\n"
"\n"
"border-radius:10px\n"
"")
        self.btn_join.setObjectName("btn_join")
        self.gridLayout.addWidget(self.btn_join, 2, 1, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(self.window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)
        self.frame = QtWidgets.QFrame(self.window)
        self.frame.setStyleSheet("border-radius:10px;\n"
"border-color: rgb(85, 170, 255);\n"
"background-color: rgb(56, 56, 56);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setContentsMargins(0, 10, 0, 10)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_img = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(100)
        self.label_img.setFont(font)
        self.label_img.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_img.setAlignment(QtCore.Qt.AlignCenter)
        self.label_img.setObjectName("label_img")
        self.gridLayout_3.addWidget(self.label_img, 0, 1, 1, 2)
        self.label_controller = QtWidgets.QLabel(self.frame)
        self.label_controller.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_controller.setAlignment(QtCore.Qt.AlignCenter)
        self.label_controller.setObjectName("label_controller")
        self.gridLayout_3.addWidget(self.label_controller, 1, 1, 1, 2)
        self.gridLayout_3.setRowStretch(0, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 15, 1)
        self.label = QtWidgets.QLabel(self.window)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.listView = QtWidgets.QListView(self.window)
        self.listView.setStyleSheet("QListView{\n"
"border: 1px solid rgb(85, 170, 255);\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"}")
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 6, 1, 1, 2)
        self.label_res = QtWidgets.QLabel(self.window)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(32)
        self.label_res.setFont(font)
        self.label_res.setStyleSheet("border: 1px solid rgb(85, 170, 255);\n"
"border-radius: 10px;\n"
"padding: 0 8px;")
        self.label_res.setAlignment(QtCore.Qt.AlignCenter)
        self.label_res.setObjectName("label_res")
        self.gridLayout.addWidget(self.label_res, 11, 1, 1, 2)
        self.gridLayout.setColumnStretch(0, 8)
        self.gridLayout_2.addWidget(self.window, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1222, 23))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.action_tutorials = QtWidgets.QAction(MainWindow)
        self.action_tutorials.setObjectName("action_tutorials")
        self.action_help = QtWidgets.QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.menu.addAction(self.action_tutorials)
        self.menu.addAction(self.action_help)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "会议手势控制"))
        self.btn_get_ctrl.setText(_translate("MainWindow", "获取控制"))
        self.label_2.setText(_translate("MainWindow", "参会人员"))
        self.btn_pause.setText(_translate("MainWindow", "开始控制"))
        self.btn_start.setText(_translate("MainWindow", "开始识别"))
        self.checkBox.setText(_translate("MainWindow", "主持人模式（本机可被控制）"))
        self.btn_join.setText(_translate("MainWindow", "加入会议"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入用户名"))
        self.label_img.setText(_translate("MainWindow", "Hellow\n"
"World"))
        self.label_controller.setText(_translate("MainWindow", "正在控制：获取中"))
        self.label.setText(_translate("MainWindow", "用户名："))
        self.label_res.setText(_translate("MainWindow", "等待手势"))
        self.menu.setTitle(_translate("MainWindow", "帮助"))
        self.action_tutorials.setText(_translate("MainWindow", "新手教学"))
        self.action_help.setText(_translate("MainWindow", "手势说明"))
