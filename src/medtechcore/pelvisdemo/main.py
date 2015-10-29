#!/usr/bin/env python
import subprocess

import sys
import threading
import Queue
import time

from PySide import QtGui

from medtechcore.pelvisdemo.mainwindow import MainWindow
from medtechcore.pelvisdemo.model.pelvis import PelvisModel


def main():

    app = QtGui.QApplication(sys.argv)

    model = PelvisModel()

    window = MainWindow(model)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()







