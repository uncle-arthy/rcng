#!/usr/bin/python3
#  -*- coding: utf-8 -*-

__author__ = 'Alexei Evdokimov'

import sys
import pprint
from sqlite_handler import DBHandler
from add_prel_run_window import AddPrelRunWindow
from run_widget import RunWidget
from edit_prel_run import EditPrelRun
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class TriWindow(QtWidgets.QWidget):
    def __init__(self, dbhandler, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self.db = dbhandler

        uic.loadUi('ui_files/runs_triscroll.ui', self)

        self.prel_runs_frame = QtWidgets.QFrame()
        self.prel_runs_vbox = QtWidgets.QVBoxLayout()
        self.prel_runs_frame.setLayout(self.prel_runs_vbox)
        self.prel_scroll_area.setWidget(self.prel_runs_frame)

        self.btn_add_prel_run.clicked.connect(self.add_prel_run)
        self.update_prel_runs()

    def add_prel_run(self):
        self.add_prel_window = AddPrelRunWindow(self.db)
        self.add_prel_window.show()
        self.add_prel_window.wannaclose.connect(self.update_prel_runs)

    def update_prel_runs(self):
        self.prel_runs_frame.destroy()

        self.prel_runs_frame = QtWidgets.QFrame()
        self.prel_runs_vbox = QtWidgets.QVBoxLayout()
        self.prel_runs_frame.setLayout(self.prel_runs_vbox)
        self.prel_scroll_area.setWidget(self.prel_runs_frame)

        prel_runs_info = self.db.get_prel_runs_info()

        if len(prel_runs_info) > 0:
            for r_num in range(1, self.db.get_next_prel_run_number()):
                run = [None, None, None, None, None]
                for info in prel_runs_info:
                    if info[3] == r_num:
                        run[0] = info[2]
                        if info[4] == 1:
                            run[1] = info
                        if info[4] == 2:
                            run[2] = info
                        if info[4] == 3:
                            run[3] = info
                        if info[4] == 4:
                            run[4] = info

                rw = RunWidget(run_type='prel', run_num=r_num, run_participants=run)
                rw.neededit.connect(self.edit_run)
                self.prel_runs_vbox.addWidget(rw)

    def edit_run(self, num):
        print('SIGNAL: ', num)
        pprint.pprint(self.db.get_participants_by_run_number(num))
        self.edit_window = EditPrelRun(self.db)
        self.edit_window.show()
        self.edit_window.wannaclose.connect(self.update_prel_runs)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dhandler = DBHandler('db/rcng_2017-07-23.db')

    MainWindow = TriWindow(dhandler)

    MainWindow.show()

    sys.exit(app.exec_())
