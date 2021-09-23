from PySide6 import QtGui, QtCore
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel

from tools.Config import Config
from tools.Signal import SignalState
from tools.Signal import Signal


class QSignalCheckedWidget(QLabel):
    def __init__(self, config: Config, signal: Signal, *args, **kwargs):
        super(QSignalCheckedWidget, self).__init__(*args, **kwargs)
        self.signal = signal
        self.config = config
        self.old_state = None

        self.color_anim = QtCore.QPropertyAnimation(self, b'backColor')
        self.updateStatus()

    def updateStatus(self):
        colorA = QColor(*self.config.get("ui.color.checking_signal", (0, 217, 255)))
        colorB = QColor(*self.config.get("ui.color.checking_signal_faded", (0, 167, 196)))

        self.color_anim.setStartValue(colorA)
        self.color_anim.setKeyValueAt(0.5, colorB)
        self.color_anim.setEndValue(colorA)
        self.color_anim.setLoopCount(-1)
        self.color_anim.start()

    def my_update(self):
        pass

    def getBackColor(self):
        return self.palette().color(QtGui.QPalette.Window)

    def setBackColor(self, color):
        self.my_update()
        if self.signal.is_been_checked:
            self.setStyleSheet("* { background: rgb(%d,%d,%d) }" % (color.red(), color.green(), color.blue()))
        else:
            self.setStyleSheet("")

    backColor = QtCore.Property(QtGui.QColor, getBackColor, setBackColor)