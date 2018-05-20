#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from sqlite_handler import DBHandler
from PyQt5 import QtCore, QtGui, QtWidgets


class AddParticipantWindow(QtWidgets.QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.db = data_handler
        self.initUI()

    def initUI(self):
        #  Decorate main window
        self.setObjectName('AddParticipantWindow')
        self.setGeometry(200, 200, 600, 300)
        self.setWindowTitle('RCNG | Register participant')

        font = QtGui.QFont()
        font.setFamily('Calibri')
        font.setPointSize(11)
        self.setFont(font)

        #  Buttons
        self.add_participant_btn = QtWidgets.QPushButton('Add participant')
        self.add_participant_btn.clicked.connect(self.add_participant_handler)
        self.commit_btn = QtWidgets.QPushButton("Commit and close")
        self.commit_btn.clicked.connect(self.commit_close)
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.add_participant_btn, 0, QtCore.Qt.AlignRight)
        self.hbox.addWidget(self.commit_btn, 0, QtCore.Qt.AlignLeft)

        #  Entry fields
        self.category_entry = QtWidgets.QComboBox()
        self.number = QtWidgets.QLineEdit()
        self.name_entry = QtWidgets.QComboBox()

        #  Layout
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow('Category:', self.category_entry)
        self.form_layout.addRow('№ in catalogue:', self.number)
        self.form_layout.addRow('Dog:', self.name_entry)

        self.form_layout.addRow(self.hbox)

        self.setLayout(self.form_layout)

        #  Set data for Categories and Dog names
        for i, category in self.db.get_categories():
            self.category_entry.addItem(category, i)

        for i, dog_name in self.db.get_ids_names():
            self.name_entry.addItem(dog_name, i)

        self.show()

    def add_participant_handler(self):
        print('Add participant...')

        participant_dict = {}
        participant_dict['dog_id'] = self.name_entry.currentData()
        participant_dict['category_id'] = self.category_entry.currentData()
        participant_dict['id'] = int(self.number.text())

        if self.db.add_participant(participant_dict):
            self.clear_fields()
        else:
            print('Something wrong!')

    def clear_fields(self):
        self.category_entry.setCurrentIndex(0)
        self.number.setText('')
        self.name_entry.setCurrentIndex(0)

    def commit_close(self):
        self.db.commit_close()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dhandler = DBHandler('db/rcng_2017-07-23.db')

    MainWindow = AddParticipantWindow(dhandler)

    MainWindow.show()

    sys.exit(app.exec_())

