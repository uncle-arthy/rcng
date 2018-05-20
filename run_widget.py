#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class RunWidget(QtWidgets.QWidget):
    neededit = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.run_number = kwargs['run_num']

        if kwargs['run_type'] == 'prel':
            uic.loadUi('ui_files/prel_run_widget.ui', self)
            self.lbl_run_number.setText(str(kwargs['run_num']))
            self.participants = kwargs['run_participants']
            self.write_prels()
            self.btn_work_on_run.clicked.connect(self.need_edit)
        else:
            uic.loadUi('ui_files/semi_run_widget.ui', self)

    def write_prels(self):
        self.lbl_category_name.setText(self.participants[0])
        self.lbl_first_name.setText(f'{self.participants[1][1]} ({self.participants[1][0]})')
        if self.participants[2]:
            self.lbl_second_name.setText(f'{self.participants[2][1]} ({self.participants[2][0]})')
        if self.participants[3]:
            self.lbl_third_name.setText(f'{self.participants[3][1]} ({self.participants[3][0]})')
        if self.participants[4]:
            self.lbl_fourth_name.setText(f'{self.participants[4][1]} ({self.participants[4][0]})')

    def need_edit(self):
        self.neededit.emit(self.run_number)


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
