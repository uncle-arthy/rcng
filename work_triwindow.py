#!/usr/bin/python3
#  -*- coding: utf-8 -*-

__author__ = 'Alexei Evdokimov'

import sys
import pprint
from sqlite_handler import DBHandler
from add_prel_run_window import AddPrelRunWindow, AddSecondRunWindow
from run_widget import RunWidget
from edit_prel_run import EditPrelRun, EditSecondRun
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

        self.semi_runs_frame = QtWidgets.QFrame()
        self.semi_runs_vbox = QtWidgets.QVBoxLayout()
        self.semi_runs_frame.setLayout(self.semi_runs_vbox)
        self.semi_scroll_area.setWidget(self.semi_runs_frame)

        self.final_runs_frame = QtWidgets.QFrame()
        self.final_runs_vbox = QtWidgets.QVBoxLayout()
        self.final_runs_frame.setLayout(self.final_runs_vbox)
        self.final_scroll_area.setWidget(self.final_runs_frame)

        self.btn_add_prel_run.clicked.connect(self.add_prel_run)
        self.btn_add_semi_run.clicked.connect(self.add_semi_run)
        self.btn_add_final_run.clicked.connect(self.add_final_run)
        self.update_prel_runs()
        self.update_semi_runs()

    def add_prel_run(self):
        self.add_prel_window = AddPrelRunWindow(self.db)
        self.add_prel_window.show()
        self.add_prel_window.wannaclose.connect(self.update_prel_runs)

    def update_prel_runs(self):
        print('update')
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

                rw = RunWidget(run_num=r_num, run_participants=run, dbhandler=self.db)
                rw.neededit.connect(self.edit_run)
                self.prel_runs_vbox.addWidget(rw)

    def edit_run(self, num, cat_name, p1, p2, p3, p4, s1, s2, s3, s4, r1, r2, r3, r4, t1, t2, t3, t4):
        self.edit_window = EditPrelRun(self.db, info=(num, cat_name, p1, p2, p3, p4, s1, s2, s3, s4, r1, r2, r3, r4, t1, t2, t3, t4))
        self.edit_window.show()
        self.edit_window.wannaclose.connect(self.update_prel_runs)

    def add_semi_run(self):
        # TODO: reimplement semifinal to FCI rules
        print('adding semi run')
        self.add_second_window = AddSecondRunWindow(self.db)
        self.add_second_window.show()
        self.add_second_window.wannaclose.connect(self.update_semi_runs)

    def update_semi_runs(self):
        print('update')
        self.semi_runs_frame.destroy()

        self.semi_runs_frame = QtWidgets.QFrame()
        self.semi_runs_vbox = QtWidgets.QVBoxLayout()
        self.semi_runs_frame.setLayout(self.semi_runs_vbox)
        self.semi_scroll_area.setWidget(self.semi_runs_frame)

        semi_runs_info = self.db.get_semi_runs_info()

        if len(semi_runs_info) > 0:
            for r_num in range(self.db.get_next_prel_run_number(), self.db.get_next_second_run_number()):
                run = [None, None, None, None, None]
                for info in semi_runs_info:
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

                rw = RunWidget(run_num=r_num, run_participants=run, dbhandler=self.db)
                rw.neededit.connect(self.edit_second_run)
                self.semi_runs_vbox.addWidget(rw)

    def edit_second_run(self, num, cat_name, p1, p2, p3, p4, s1, s2, s3, s4, r1, r2, r3, r4, t1, t2, t3, t4):
        self.edit_window = EditSecondRun(self.db, info=(num, cat_name, p1, p2, p3, p4, s1, s2, s3, s4, r1, r2, r3, r4, t1, t2, t3, t4))
        self.edit_window.show()
        self.edit_window.wannaclose.connect(self.update_semi_runs)

    def add_final_run(self):
        print('adding final run')
        cat_names = [c[1] for c in self.db.get_categories()]

        cat_choose, ok = QtWidgets.QInputDialog.getItem(self, 'Final Run for...', 'Choose', cat_names)

        if ok:
            print(cat_names.index(cat_choose) + 1)
            print(cat_choose)
            if self.db.add_final_run(cat_names.index(cat_choose) + 1):
                self.update_final_runs()

    def update_final_runs(self):
        print('update')
        self.semi_runs_frame.destroy()

        self.final_runs_frame = QtWidgets.QFrame()
        self.final_runs_vbox = QtWidgets.QVBoxLayout()
        self.final_runs_frame.setLayout(self.final_runs_vbox)
        self.final_scroll_area.setWidget(self.final_runs_frame)

        final_runs_info = self.db.get_final_runs_info()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dhandler = DBHandler('db/rcng_2017-07-23.db')

    MainWindow = TriWindow(dhandler)

    MainWindow.show()

    sys.exit(app.exec_())
