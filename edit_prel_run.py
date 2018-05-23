#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import pprint
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class EditPrelRun (QtWidgets.QWidget):
    wannaclose = QtCore.pyqtSignal()

    def __init__(self, dbhandler, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self.db = dbhandler
        self.num = kwargs['info'][0]
        self.cat_name = kwargs['info'][1]
        self.num_1 = kwargs['info'][2]
        self.name_1 = kwargs['info'][6]
        self.num_2 = kwargs['info'][3]
        self.name_2 = kwargs['info'][7]
        self.num_3 = kwargs['info'][4]
        self.name_3 = kwargs['info'][8]
        self.num_4 = kwargs['info'][5]
        self.name_4 = kwargs['info'][9]
        self.status_1 = kwargs['info'][10] - 1 if kwargs['info'][10] != 1 else 1
        self.status_2 = kwargs['info'][11] - 1 if kwargs['info'][11] != 1 else 1
        self.status_3 = kwargs['info'][12] - 1 if kwargs['info'][12] != 1 else 1
        self.status_4 = kwargs['info'][13] - 1 if kwargs['info'][13] != 1 else 1

        self.statuses = self.db.get_statuses()

        uic.loadUi('ui_files/time_register_widget.ui', self)

        self.lbl_run_number.setText(str(self.num))
        self.lbl_category_name.setText(self.cat_name)
        self.lbl_first_name.setText(self.name_1)
        self.lbl_second_name.setText(self.name_2)
        self.lbl_third_name.setText(self.name_3)
        self.lbl_fourth_name.setText(self.name_4)

        for i, res in self.statuses:
            self.cb_first_status.addItem(res, i)
            self.cb_second_status.addItem(res, i)
            self.cb_third_status.addItem(res, i)
            self.cb_fourth_status.addItem(res, i)
        self.cb_first_status.setCurrentIndex(self.status_1)
        self.cb_second_status.setCurrentIndex(self.status_2)
        self.cb_third_status.setCurrentIndex(self.status_3)
        self.cb_fourth_status.setCurrentIndex(self.status_4)

        self.inp_first_time.setText(kwargs['info'][14])
        self.inp_second_time.setText(kwargs['info'][15])
        self.inp_third_time.setText(kwargs['info'][16])
        self.inp_fourth_time.setText(kwargs['info'][17])

        if not self.num_2:
            self.inp_second_time.setEnabled(False)
            self.cb_second_status.setEnabled(False)
        if not self.num_3:
            self.inp_third_time.setEnabled(False)
            self.cb_third_status.setEnabled(False)
        if not self.num_4:
            self.inp_fourth_time.setEnabled(False)
            self.cb_fourth_status.setEnabled(False)

        self.btn_register_time.clicked.connect(self.register_times)
        self.btn_delete_run.clicked.connect(self.delete_run)

    def register_times(self):
        reg_info = {}

        all_good = True

        reg_info['run_num'] = self.num
        reg_info['num_1'] = self.num_1
        try:
            reg_info['time_1'] = int(self.inp_first_time.text().replace('.', ''))
        except:
            self.warn = QtWidgets.QMessageBox.information(self, 'Error', 'Please, fill first time correctly')
            all_good = False
        reg_info['status_1'] = self.cb_first_status.currentData()

        if self.num_2:
            reg_info['num_2'] = self.num_2
            try:
                reg_info['time_2'] = int(self.inp_second_time.text().replace('.', ''))
            except:
                self.warn = QtWidgets.QMessageBox.information(self, 'Error', 'Please, fill second time correctly')
                all_good = False
            reg_info['status_2'] = self.cb_second_status.currentData()
        else:
            reg_info['num_2'] = 0

        if self.num_3:
            reg_info['num_3'] = self.num_3
            try:
                reg_info['time_3'] = int(self.inp_third_time.text().replace('.', ''))
            except:
                self.warn = QtWidgets.QMessageBox.information(self, 'Error', 'Please, fill third time correctly')
                all_good = False
            reg_info['status_3'] = self.cb_third_status.currentData()
        else:
            reg_info['num_3'] = 0

        if self.num_4:
            reg_info['num_4'] = self.num_4
            try:
                reg_info['time_4'] = int(self.inp_fourth_time.text().replace('.', ''))
            except:
                self.warn = QtWidgets.QMessageBox.information(self, 'Error', 'Please, fill fourth time correctly')
                all_good = False
            reg_info['status_4'] = self.cb_fourth_status.currentData()
        else:
            reg_info['num_4'] = 0

        if all_good:
            print('HURRAY!')
            pprint.pprint(reg_info)
            if self.db.register_time_prel_run(reg_info):
                self.wannaclose.emit()
                self.close()

    def delete_run(self):
        answer = QtWidgets.QMessageBox.question(self, 'Delete run', "Really delete this run?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            if self.db.delete_run(self.num):
                self.wannaclose.emit()
                self.close()


class EditSecondRun (QtWidgets.QWidget):
    wannaclose = QtCore.pyqtSignal()

    def __init__(self, dbhandler, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self.db = dbhandler
        self.num = kwargs['info'][0]
        self.cat_name = kwargs['info'][1]
        self.num_1 = kwargs['info'][2]
        self.name_1 = kwargs['info'][6]
        self.num_2 = kwargs['info'][3]
        self.name_2 = kwargs['info'][7]
        self.num_3 = kwargs['info'][4]
        self.name_3 = kwargs['info'][8]
        self.num_4 = kwargs['info'][5]
        self.name_4 = kwargs['info'][9]
        self.status_1 = kwargs['info'][10] - 1 if kwargs['info'][10] != 1 else 1
        self.status_2 = kwargs['info'][11] - 1 if kwargs['info'][11] != 1 else 1
        self.status_3 = kwargs['info'][12] - 1 if kwargs['info'][12] != 1 else 1
        self.status_4 = kwargs['info'][13] - 1 if kwargs['info'][13] != 1 else 1

        self.statuses = self.db.get_statuses()

        uic.loadUi('ui_files/time_register_widget.ui', self)

        self.lbl_run_number.setText(str(self.num))
        self.lbl_category_name.setText(self.cat_name)
        self.lbl_first_name.setText(self.name_1)
        self.lbl_second_name.setText(self.name_2)
        self.lbl_third_name.setText(self.name_3)
        self.lbl_fourth_name.setText(self.name_4)

        for i, res in self.statuses:
            self.cb_first_status.addItem(res, i)
            self.cb_second_status.addItem(res, i)
            self.cb_third_status.addItem(res, i)
            self.cb_fourth_status.addItem(res, i)
        self.cb_first_status.setCurrentIndex(self.status_1)
        self.cb_second_status.setCurrentIndex(self.status_2)
        self.cb_third_status.setCurrentIndex(self.status_3)
        self.cb_fourth_status.setCurrentIndex(self.status_4)

        self.inp_first_time.setText(kwargs['info'][14])
        self.inp_second_time.setText(kwargs['info'][15])
        self.inp_third_time.setText(kwargs['info'][16])
        self.inp_fourth_time.setText(kwargs['info'][17])

        if not self.num_2:
            self.inp_second_time.setEnabled(False)
            self.cb_second_status.setEnabled(False)
        if not self.num_3:
            self.inp_third_time.setEnabled(False)
            self.cb_third_status.setEnabled(False)
        if not self.num_4:
            self.inp_fourth_time.setEnabled(False)
            self.cb_fourth_status.setEnabled(False)

        self.btn_register_time.clicked.connect(self.register_times)
        self.btn_delete_run.clicked.connect(self.delete_run)

    def register_times(self):
        reg_info = {}

        all_good = True

        reg_info['run_num'] = self.num
        reg_info['num_1'] = self.num_1
        try:
            reg_info['time_1'] = int(self.inp_first_time.text().replace('.', ''))
        except:
            self.warn = QtWidgets.QMessageBox.information(self, 'Error', 'Please, fill first time correctly')
            all_good = False
        reg_info['status_1'] = self.cb_first_status.currentData()

        if self.num_2:
            reg_info['num_2'] = self.num_2
            try:
                reg_info['time_2'] = int(self.inp_second_time.text().replace('.', ''))
            except:
                self.warn = QtWidgets.QMessageBox.information(self, 'Error', 'Please, fill second time correctly')
                all_good = False
            reg_info['status_2'] = self.cb_second_status.currentData()
        else:
            reg_info['num_2'] = 0

        if self.num_3:
            reg_info['num_3'] = self.num_3
            try:
                reg_info['time_3'] = int(self.inp_third_time.text().replace('.', ''))
            except:
                self.warn = QtWidgets.QMessageBox.information(self, 'Error', 'Please, fill third time correctly')
                all_good = False
            reg_info['status_3'] = self.cb_third_status.currentData()
        else:
            reg_info['num_3'] = 0

        if self.num_4:
            reg_info['num_4'] = self.num_4
            try:
                reg_info['time_4'] = int(self.inp_fourth_time.text().replace('.', ''))
            except:
                self.warn = QtWidgets.QMessageBox.information(self, 'Error', 'Please, fill fourth time correctly')
                all_good = False
            reg_info['status_4'] = self.cb_fourth_status.currentData()
        else:
            reg_info['num_4'] = 0

        if all_good:
            print('HURRAY!')
            pprint.pprint(reg_info)
            if self.db.register_time_second_run(reg_info):
                self.wannaclose.emit()
                self.close()

    def delete_run(self):
        answer = QtWidgets.QMessageBox.question(self, 'Delete run', "Really delete this run?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            if self.db.delete_semi_run(self.num):
                self.wannaclose.emit()
                self.close()

