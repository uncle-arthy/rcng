#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from sqlite_handler import DBHandler
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class AddPrelRunWindow(QtWidgets.QWidget):
    wannaclose = QtCore.pyqtSignal()

    def __init__(self, dbhandler, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self.db = dbhandler

        uic.loadUi('ui_files/register_prel_run.ui', self)

        self.update_fields()

        self.btn_add_run.clicked.connect(self.add_run)

    def update_fields(self):
        self.inp_run_number.setValue(self.db.get_next_prel_run_number())

        for i, category in self.db.get_categories():
            self.cb_category.addItem(category, i)

        self.cb_category.activated.connect(self.update_dog_names_from_category)

    def update_dog_names_from_category(self, t):
        dog_names_list = self.db.get_dog_for_prel_run(t+1)

        for i, name in dog_names_list:
            print(i, name)

        self.cb_first_dog.clear()
        self.cb_second_dog.clear()
        self.cb_third_dog.clear()
        self.cb_fourth_dog.clear()

        self.cb_first_dog.addItem('', 0)
        self.cb_second_dog.addItem('', 0)
        self.cb_third_dog.addItem('', 0)
        self.cb_fourth_dog.addItem('', 0)

        for i, name in dog_names_list:
            self.cb_first_dog.addItem(name, i)
            self.cb_second_dog.addItem(name, i)
            self.cb_third_dog.addItem(name, i)
            self.cb_fourth_dog.addItem(name, i)

    def add_run(self):
        run = {}
        run['num'] = self.inp_run_number.value()
        run['cat_id'] = self.cb_category.currentData()
        run['first_id'] = self.cb_first_dog.currentData()
        run['second_id'] = self.cb_second_dog.currentData()
        run['third_id'] = self.cb_third_dog.currentData()
        run['fourth_id'] = self.cb_fourth_dog.currentData()

        print(run)
        if self.db.register_prel_run(run):
            print('Run added')
            self.wannaclose.emit()
            self.close()
        else:
            print('Something wrong. Run not added.')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dhandler = DBHandler('db/rcng_2017-07-23.db')

    MainWindow = AddPrelRunWindow(dhandler)

    MainWindow.show()

    sys.exit(app.exec_())
