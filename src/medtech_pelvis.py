#!/usr/bin/env python

import sys

from PySide import QtGui

from mainwindow import MainWindow
from model.pelvis import PelvisModel


def main():

    app = QtGui.QApplication(sys.argv)

    model = PelvisModel()

    window = MainWindow(model)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()







