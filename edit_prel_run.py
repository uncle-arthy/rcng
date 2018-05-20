#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sys
from sqlite_handler import DBHandler
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class EditPrelRun (QtWidgets.QWidget):
    wannaclose = QtCore.pyqtSignal()

    def __init__(self, dbhandler, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self.db = dbhandler

        uic.loadUi('ui_files/time_register_widget.ui', self)
