#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class RunWidget(QtWidgets.QWidget):
    neededit = QtCore.pyqtSignal(int, str, int, int, int, int, str, str, str, str, int, int, int, int, str, str, str, str)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.run_number = kwargs['run_num']
        self.db = kwargs['dbhandler']
        self.results = self.db.get_statuses()

        uic.loadUi('ui_files/prel_run_widget.ui', self)
        self.lbl_run_number.setText(str(kwargs['run_num']))
        self.participants = kwargs['run_participants']
        self.lbl_category_name.setText(self.participants[0])
        self.write_prels()
        self.btn_work_on_run.clicked.connect(self.need_edit)

    def write_prels(self):
        self.lbl_first_name.setText(f'{self.participants[1][1]} ({self.participants[1][0]})')
        if self.participants[1][6] == 2:
            self.lbl_first_result.setText(self.pretty_time(self.participants[1][5]))
        elif self.participants[1][6] in (4, 5, 6):
            self.lbl_first_result.setText(self.result_name(self.participants[1][6]))
        else:
            self.lbl_first_result.setText(' ')

        if self.participants[2]:
            self.lbl_second_name.setText(f'{self.participants[2][1]} ({self.participants[2][0]})')
            if self.participants[2][6] == 2:
                self.lbl_second_result.setText(self.pretty_time(self.participants[2][5]))
            elif self.participants[2][6] in (4, 5, 6):
                self.lbl_second_result.setText(self.result_name(self.participants[2][6]))
            else:
                self.lbl_second_result.setText(' ')
        if self.participants[3]:
            self.lbl_third_name.setText(f'{self.participants[3][1]} ({self.participants[3][0]})')
            if self.participants[3][6] == 2:
                self.lbl_third_result.setText(self.pretty_time(self.participants[3][5]))
            elif self.participants[3][6] in (4, 5, 6):
                self.lbl_third_result.setText(self.result_name(self.participants[3][6]))
            else:
                self.lbl_third_result.setText(' ')
        if self.participants[4]:
            self.lbl_fourth_name.setText(f'{self.participants[4][1]} ({self.participants[4][0]})')
            if self.participants[4][6] == 2:
                self.lbl_fourth_result.setText(self.pretty_time(self.participants[4][5]))
            elif self.participants[4][6] in (4, 5, 6):
                self.lbl_fourth_result.setText(self.result_name(self.participants[4][6]))
            else:
                self.lbl_fourth_result.setText(' ')

    def need_edit(self):
        second = self.participants[2][0] if self.participants[2] else 0
        second_name = self.participants[2][1] if self.participants[2] else '---'
        second_rslt = self.participants[2][6] if self.participants[2] else 3
        second_time = self.pretty_time(self.participants[2][5]) if self.participants[2] else ''
        third = self.participants[3][0] if self.participants[3] else 0
        third_name = self.participants[3][1] if self.participants[3] else '---'
        third_rslt = self.participants[3][6] if self.participants[3] else 3
        third_time = self.pretty_time(self.participants[3][5]) if self.participants[3] else ''
        fourth = self.participants[4][0] if self.participants[4] else 0
        fourth_name = self.participants[4][1] if self.participants[4] else '---'
        fourth_rslt = self.participants[4][6] if self.participants[4] else 3
        fourth_time = self.pretty_time(self.participants[4][5]) if self.participants[4] else ''
        self.neededit.emit(self.run_number,
                           self.participants[0],
                           self.participants[1][0],
                           second,
                           third,
                           fourth,
                           self.participants[1][1],
                           second_name,
                           third_name,
                           fourth_name,
                           self.participants[1][6],
                           second_rslt,
                           third_rslt,
                           fourth_rslt,
                           self.pretty_time(self.participants[1][5]),
                           second_time,
                           third_time,
                           fourth_time)

    def result_name(self, res_num):
        if res_num == 4:
            return 'DSQ'
        if res_num == 5:
            return 'CB'
        if res_num == 6:
            return 'C'
        return 'N/A'

    def pretty_time(self, time_int):
        s = str(time_int)

        return s[:-2] + '.' + s[-2:]


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
