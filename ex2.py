# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ex2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from pyqtgraph import ImageView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
import cv2


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1040, 835)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pb1 = QtWidgets.QPushButton(self.centralwidget)
        self.pb1.setGeometry(QtCore.QRect(30, 30, 211, 61))
        self.pb1.setObjectName("pb1")
        self.lb1 = QtWidgets.QLabel(self.centralwidget)
        self.lb1.setGeometry(QtCore.QRect(270, 30, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.lb1.setFont(font)
        self.lb1.setObjectName("lb1")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(40, 110, 70, 17))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(40, 140, 70, 17))
        self.checkBox_2.setObjectName("checkBox_2")
        self.lb2 = QtWidgets.QLabel(self.centralwidget)
        self.lb2.setGeometry(QtCore.QRect(490, 40, 341, 331))
        self.lb2.setText("")
        self.lb2.setPixmap(QtGui.QPixmap(
            "C:/Users/USER/Desktop/New folder/Frames From Data00962/Data00962 0144.tif"))
        self.lb2.setScaledContents(True)
        self.lb2.setObjectName("lb2")
        self.pbP = QtWidgets.QPushButton(self.centralwidget)
        self.pbP.setGeometry(QtCore.QRect(850, 60, 131, 41))
        self.pbP.setObjectName("pbP")
        self.pbN = QtWidgets.QPushButton(self.centralwidget)
        self.pbN.setGeometry(QtCore.QRect(850, 120, 111, 51))
        self.pbN.setObjectName("pbN")
        self.comboX = QtWidgets.QComboBox(self.centralwidget)
        self.comboX.setGeometry(QtCore.QRect(20, 210, 211, 161))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboX.setFont(font)
        self.comboX.setObjectName("comboX")
        self.comboX.addItem("")
        self.comboX.addItem("")
        self.comboY = QtWidgets.QComboBox(self.centralwidget)
        self.comboY.setGeometry(QtCore.QRect(20, 410, 211, 161))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboY.setFont(font)
        self.comboY.setObjectName("comboY")
        self.comboY.addItem("")
        self.comboY.addItem("")
        self.submit = QtWidgets.QPushButton(self.centralwidget)
        self.submit.setGeometry(QtCore.QRect(20, 600, 131, 61))
        self.submit.setObjectName("submit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 690, 301, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.graphicsView = ImageView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(430, 390, 441, 361))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1040, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionNew.triggered.connect(lambda: self.clicked("New was clicked"))
        self.actionCopy.triggered.connect(lambda: self.clicked("copy was clicked"))
        self.actionSave.triggered.connect(lambda: self.clicked("save was clicked"))
        self.actionPaste.triggered.connect(lambda: self.clicked("paste was clicked"))
        self.pbP.clicked.connect(self.show_popup)

        self.submit.clicked.connect(self.pressed)

        self.pbP.clicked.connect(lambda: self.Imshow())
        self.pbN.clicked.connect(lambda: self.Imshow2())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pb1.setText(_translate("MainWindow", "Press ME"))
        self.lb1.setText(_translate("MainWindow", "Hello Program"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.pbP.setText(_translate("MainWindow", "Previous"))
        self.pbN.setText(_translate("MainWindow", "Next"))
        self.comboX.setItemText(0, _translate("MainWindow", "0"))
        self.comboX.setItemText(1, _translate("MainWindow", "1"))
        self.comboY.setItemText(0, _translate("MainWindow", "0"))
        self.comboY.setItemText(1, _translate("MainWindow", "1"))
        self.submit.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "X XOR Y = "))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Create a New file"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setStatusTip(_translate("MainWindow", "copy a file"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setStatusTip(_translate("MainWindow", "Paste a file"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.pbP.clicked.connect(self.show_previous)
        self.pbN.clicked.connect(self.show_next)
        self.pbP.setText(_translate("MainWindow", "Show Popup"))

    def clicked(self, text):
        self.lb1.setText(text)
        self.lb1.adjustSize()

    def show_previous(self):
        self.lb2.setPixmap(QtGui.QPixmap(
            "C:/Users/USER/Desktop/New folder/Frames From Data00962/Data00962 0144.tif"))

    def show_next(self):
        self.lb2.setPixmap(QtGui.QPixmap(
            "C:/Users/USER/Desktop/New folder/Frames From Data00962/Data00962 0155.tif"))

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Example QT5")
        msg.setText("This is the main text")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry | QMessageBox.Ignore)
        msg.setDefaultButton(QMessageBox.Ignore)
        msg.setInformativeText("Informative text")

        msg.setDetailedText("details")

        msg.buttonClicked.connect(self.popup_button)

        x = msg.exec_()

    def popup_button(self, i):
        print(i.text())

    def pressed(self):
        x = int(self.comboX.currentText())
        y = int(self.comboY.currentText())
        xor = (x and not y) or (not x and y)
        if xor == True:
            xor = 1
        else:
            xor = 0
        self.label.setText("X XOR Y = " + str(xor))

    def Imshow(self):
        self.iv = pg.imageview.ImageView()
        Reference = cv2.imread('F:/NATIONAL TAIPEI UNIVERSITY OF TECHNOLOGY'
                               '/CASES AND RESULT/image for histogram matching'
                               '/Frames From New Project2/New Project2 0091.tif', -1)
        Reference = cv2.cvtColor(Reference, cv2.COLOR_BGR2RGB)
        self.iv.setLevels(0, 256)
        self.hist = self.iv.getHistogramWidget()
        self.hist.vb.enableAutoRange(self.hist.vb.YAxis, False)
        self.graphicsView.show()
        self.graphicsView.setImage(Reference)

    def Imshow2(self):
        self.iv = pg.imageview.ImageView()
        Reference2 = cv2.imread(
            'C:/Users/USER/Desktop/New folder/Frames From Data00962/Data00962 0144.tif', -1)
        # Reference2 = cv2.imread(
        #    'C:/Users/USER/Pictures/121288.jpg', -1)
        Reference2 = cv2.cvtColor(Reference2, cv2.COLOR_BGR2RGB)
        print(Reference2.shape)
        #self.iv.setLevels(0, 256)
        #self.hist = self.iv.getHistogramWidget()
        #self.hist.vb.enableAutoRange(self.hist.vb.YAxis, False)
        #self.graphicsView.setLevels(0, 3600)
        self.graphicsView.show()
        self.graphicsView.setImage(Reference2)
        self.graphicsView.ui.histogram.hide()
        # self.graphicsView.histogram.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
