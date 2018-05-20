#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class RunWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        if kwargs['run_type'] == 'prel':
            uic.loadUi('ui_files/prel_run_widget.ui', self)
            self.lbl_first_name.setText("FIRST")
            self.lbl_run_number.setText(str(kwargs['run_num']))
        else:
            uic.loadUi('ui_files/semi_run_widget.ui', self)


class Runs(QtWidgets.QWidget):
    def __init__(self, datahandler=None, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        uic.loadUi('ui_files/runs_triscroll.ui', self)
        self.db = datahandler


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # run = RunWidget(run_type='prel')
    # run = RunWidget(run_type='semi')

    # run.show()
    runs = Runs()
    fr = QtWidgets.QFrame()
    vbox = QtWidgets.QVBoxLayout()
    fr.setLayout(vbox)
    for i in range(20):
        r = RunWidget(run_type='prel', run_num=i)
        vbox.addWidget(r)

    runs.prel_scroll_area.setWidget(fr)
    runs.show()

    sys.exit(app.exec_())
