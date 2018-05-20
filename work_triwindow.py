#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from sqlite_handler import DBHandler
from add_prel_run_window import AddPrelRunWindow
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class TriWindow(QtWidgets.QWidget):
    def __init__(self, dbhandler, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self.db = dbhandler

        uic.loadUi('ui_files/runs_triscroll.ui', self)

        self.btn_add_prel_run.clicked.connect(self.add_prel_run)

    def add_prel_run(self):
        print('Add Prel')
        self.add_prel_window = AddPrelRunWindow(self.db)
        self.add_prel_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dhandler = DBHandler('db/rcng_2017-07-23.db')

    MainWindow = TriWindow(dhandler)

    MainWindow.show()

    sys.exit(app.exec_())
