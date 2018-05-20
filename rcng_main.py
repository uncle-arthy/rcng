#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from work_triwindow import TriWindow
from sqlite_handler import DBHandler
from summary import SummaryWindow
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class RSNG(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.db = None
        uic.loadUi('ui_files/main_window.ui', self)

        self.actionOpen.triggered.connect(self.openDB)
        self.actionSummary.triggered.connect(self.show_summary)
        self.actionExit.triggered.connect(self.close_program)
        self.actionAbout.triggered.connect(self.about_window)

    def openDB(self):
        db_file = QtWidgets.QFileDialog.getOpenFileName()
        db_path = db_file[0]

        self.db = DBHandler(db_path)

        self.start_work()

    def start_work(self):
        triwin = TriWindow(self.db)
        self.setCentralWidget(triwin)

    def show_summary(self):
        self.sum_window = SummaryWindow(self.db)
        self.sum_window.show()

    def close_program(self):
        print("Finish all")
        if self.db:
            self.db.commit_close()
        self.close()

    def about_window(self):
        print('Here goes About...')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = RSNG()

    MainWindow.show()

    sys.exit(app.exec_())
