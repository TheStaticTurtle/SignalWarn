from PySide6 import QtGui, QtCore
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel

from tools.Signal import SignalState
from tools.Signal import Signal


class QSignalStatusWidget(QLabel):
    def __init__(self, signal: Signal, *args, **kwargs):
        super(QSignalStatusWidget, self).__init__(*args, **kwargs)
        self.signal = signal
        self.old_state = None

        self.color_anim = QtCore.QPropertyAnimation(self, b'backColor')
        self.updateStatus()

    def updateStatus(self):
        self.color_anim.stop()

        colorA = colorB = QColor(70, 70, 70)
        if self.signal.state == SignalState.ABSENT:
            colorA = QColor(255, 0, 0)
            colorB = QColor(100, 0, 0)
        if self.signal.state == SignalState.MUTED:
            colorA = QColor(255, 100, 0)
            colorB = QColor(100, 50, 0)
        if self.signal.state == SignalState.UNKNOWN:
            colorA = QColor(70, 70, 70)
            colorB = QColor(100, 100, 100)
        if self.signal.state == SignalState.NORMAL:
            colorA = colorB = QColor(0, 255, 0)

        self.setBackColor(colorA)

        self.color_anim.setStartValue(colorA)
        self.color_anim.setKeyValueAt(0.5, colorB)
        self.color_anim.setEndValue(colorA)
        self.color_anim.setLoopCount(-1)
        self.color_anim.start()

        self.setText(str(self.signal.state))

    def getBackColor(self):
        return self.palette().color(QtGui.QPalette.Window)

    def setBackColor(self, color):
        self.setStyleSheet("* { background: rgb(%d,%d,%d) }" % (color.red(), color.green(), color.blue()))

        if self.signal.state != self.old_state:
            self.old_state = self.signal.state
            self.updateStatus()

    backColor = QtCore.Property(QtGui.QColor, getBackColor, setBackColor)