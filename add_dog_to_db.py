#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from sqlite_handler import DBHandler
from PyQt5 import QtCore, QtGui, QtWidgets


class AddDogWindow(QtWidgets.QWidget):
    def __init__(self, datahandler):
        super().__init__()
        self.db = datahandler
        self.initUI()

    def initUI(self):

        #  Decorate main window
        self.setObjectName('AddDogWindow')
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle('RCNG | Add dog to DB')

        font = QtGui.QFont()
        font.setFamily('Calibri')
        font.setPointSize(11)
        self.setFont(font)

        # Service text
        self.service_label = QtWidgets.QLabel("\nThis is service label\n\n")
        self.service_label.setAlignment(QtCore.Qt.AlignCenter)

        # Buttons
        self.add_dog_to_db_btn = QtWidgets.QPushButton("Add to DB")
        self.add_dog_to_db_btn.clicked.connect(self.add_dog_handler)
        self.commit_btn = QtWidgets.QPushButton("Commit and close")
        self.commit_btn.clicked.connect(self.commit_close)
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.add_dog_to_db_btn, 0, QtCore.Qt.AlignRight)
        self.hbox.addWidget(self.commit_btn, 0, QtCore.Qt.AlignLeft)

        # Entry fields
        self.dog_name_entry = QtWidgets.QLineEdit()
        self.dog_breed_entry = QtWidgets.QComboBox()
        self.dog_gender_entry = QtWidgets.QComboBox()
        self.dog_owner_entry = QtWidgets.QLineEdit()
        self.dog_birth_entry = QtWidgets.QDateEdit()
        self.dog_birth_entry.setDisplayFormat("dd.MM.yyyy")
        self.dog_doc_entry = QtWidgets.QLineEdit()
        self.dog_racebook_entry = QtWidgets.QLineEdit()
        self.dog_tattoo_entry = QtWidgets.QLineEdit()
        self.dog_comments_entry = QtWidgets.QLineEdit()

        # Layout
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow(self.service_label)
        self.form_layout.addRow("Dog name:", self.dog_name_entry)
        self.form_layout.addRow("Breed:", self.dog_breed_entry)
        self.form_layout.addRow("Gender", self.dog_gender_entry)
        self.form_layout.addRow("Owner:", self.dog_owner_entry)
        self.form_layout.addRow("Birth date:", self.dog_birth_entry)
        self.form_layout.addRow("№ doc:", self.dog_doc_entry)
        self.form_layout.addRow("№ racebook:", self.dog_racebook_entry)
        self.form_layout.addRow("Tattoo:", self.dog_tattoo_entry)
        self.form_layout.addRow("Comments:", self.dog_comments_entry)

        self.form_layout.addRow(self.hbox)

        self.setLayout(self.form_layout)

        # Set data for Breeds etc.
        for i, breed in self.db.get_breeds():
            self.dog_breed_entry.addItem(breed, i)

        self.dog_gender_entry.addItem("Male", 1)
        self.dog_gender_entry.addItem("Female", 2)

        self.show()

    def add_dog_handler(self):
        print("Adding Dog...")

        dog_dict = {}
        dog_dict["name"] = self.dog_name_entry.text()
        dog_dict["breed_id"] = self.dog_breed_entry.currentData()
        dog_dict["breed_name"] = self.dog_breed_entry.currentText()
        dog_dict["gender_id"] = self.dog_gender_entry.currentData()
        dog_dict["owner"] = self.dog_owner_entry.text()
        dog_dict["birthday"] = self.dog_birth_entry.date().toPyDate().strftime("%Y-%m-%d")
        dog_dict["doc"] = self.dog_doc_entry.text()
        dog_dict["racebook"] = self.dog_racebook_entry.text()
        dog_dict["tattoo"] = self.dog_tattoo_entry.text()
        dog_dict["comments"] = self.dog_comments_entry.text()

        if self.db.add_dog_to_db(dog_dict):
            self.clear_fields()
        else:
            print('Something wrong!')

    def clear_fields(self):
        self.dog_name_entry.setText('')
        self.dog_breed_entry.setCurrentIndex(0)
        self.dog_gender_entry.setCurrentIndex(0)
        self.dog_owner_entry.setText('')
        self.dog_doc_entry.setText('')
        self.dog_racebook_entry.setText('')
        self.dog_tattoo_entry.setText('')
        self.dog_comments_entry.setText('')

    def commit_close(self):
        self.db.commit_close()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dhandler = DBHandler('db/rcng_2017-07-23.db')

    MainWindow = AddDogWindow(dhandler)

    MainWindow.show()

    sys.exit(app.exec_())
