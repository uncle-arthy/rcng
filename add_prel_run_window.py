#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from sqlite_handler import DBHandler
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class AddPrelRunWindow(QtWidgets.QWidget):
    def __init__(self, dbhandler, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self.db = dbhandler

        uic.loadUi('ui_files/register_prel_run.ui', self)

        self.update_fields()

    def update_fields(self):
        self.inp_run_number.setValue(self.db.get_next_prel_run_number())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dhandler = DBHandler('db/rcng_2017-07-23.db')

    MainWindow = AddPrelRunWindow(dhandler)

    MainWindow.show()

    sys.exit(app.exec_())
