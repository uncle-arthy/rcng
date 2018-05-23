#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from sqlite_handler import DBHandler
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class SummaryWindow(QtWidgets.QWidget):
    def __init__(self, dbhandler, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self.db = dbhandler

        uic.loadUi('ui_files/summary_second_window.ui', self)

        self.btn_refresh.clicked.connect(self.fill_up_table)
        self.btn_make_places.clicked.connect(self.update_places)

        self.pretty_table()
        self.fill_up_table()

    def pretty_table(self):
        self.summaryTable.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignHCenter)
        self.summaryTable.horizontalHeaderItem(3).setTextAlignment(QtCore.Qt.AlignHCenter)
        self.summaryTable.horizontalHeaderItem(4).setTextAlignment(QtCore.Qt.AlignHCenter)
        self.summaryTable.horizontalHeaderItem(5).setTextAlignment(QtCore.Qt.AlignHCenter)
        self.summaryTable.horizontalHeaderItem(6).setTextAlignment(QtCore.Qt.AlignHCenter)
        self.summaryTable.horizontalHeaderItem(7).setTextAlignment(QtCore.Qt.AlignHCenter)
        self.summaryTable.horizontalHeaderItem(8).setTextAlignment(QtCore.Qt.AlignHCenter)

        header = self.summaryTable.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def fill_up_table(self):
        sum_list = self.db.get_second_participants_summary()

        self.summaryTable.setRowCount(len(sum_list))

        for i, participant in enumerate(sum_list):
            for j in range(9):
                self.summaryTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(participant[j])))
                self.summaryTable.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.summaryTable.item(i, 1).setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.summaryTable.item(i, 2).setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

    def update_places(self):
        self.db.update_places()
        self.fill_up_table()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dhandler = DBHandler('db/rcng_2017-07-23.db')

    MainWindow = SummaryWindow(dhandler)

    MainWindow.show()

    sys.exit(app.exec_())
