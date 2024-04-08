import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import PyQt5
import pandas as pd


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        loadUi(r'D:\DSAFinalProject\UI\admin.ui', self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.showMaximized()
    sys.exit(app.exec_())
