#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original Author: Vitus Maierhöfer
# Refactored and adjusted by: Jürgen Hahn

import sys
import csv
from PyQt5 import QtWidgets, uic
import os

UI_FILE = 'nasa-tlx.ui'
LOG_DIRECTORY = 'log/'


class NasaTLX(QtWidgets.QWizard):
    def __init__(self):
        super().__init__()

        self.pid = sys.argv[1]
        self.system = sys.argv[2]
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi(UI_FILE, self)
        self.showFullScreen()

        if QtWidgets.QWizard.currentId(self) != 1:
            self.button(QtWidgets.QWizard.BackButton).hide()
        else:
            self.button(QtWidgets.QWizard.BackButton).show()

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_finished)
        self.show()

    def on_finished(self):
        self.write_to_csv()

    def write_to_csv(self):
        if not os.path.exists(LOG_DIRECTORY):
            os.makedirs(LOG_DIRECTORY)

        out_file = open(LOG_DIRECTORY + 'tlx_participant' + str(self.pid) + '_system' + str(self.system) + '.csv', mode='a+')

        print("pid,sys,mental,physical,temporal,performance,effort,frustration", file=out_file)
        print(f"{self.pid},"
              f"{self.system},"
              f"{self.ui.slider_mental.value()},"
              f"{self.ui.slider_physical.value()},"
              f"{self.ui.slider_temporal.value()},"
              f"{self.ui.slider_performance.value()},"
              f"{self.ui.slider_effort.value()},"
              f"{self.ui.slider_frustration.value()}", file=out_file)

        out_file.close()


def main():
    if len(sys.argv) != 3: # change for your puproses
        print("Usage: python3 ntlx.py <pid> <system_id_or_name>")

    app = QtWidgets.QApplication(sys.argv)
    NasaTLX()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
