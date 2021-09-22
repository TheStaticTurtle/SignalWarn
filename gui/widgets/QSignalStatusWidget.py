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
            colorA = QColor(252, 186, 3)
            colorB = QColor(156, 115, 3)
        if self.signal.state == SignalState.UNKNOWN:
            colorA = QColor(70, 70, 70)
            colorB = QColor(100, 100, 100)
        if self.signal.state == SignalState.NORMAL:
            colorA = colorB = QColor(87, 181, 54)

        self.setBackColor(colorA)

        self.color_anim.setStartValue(colorA)
        self.color_anim.setKeyValueAt(0.5, colorB)
        self.color_anim.setEndValue(colorA)
        self.color_anim.setLoopCount(-1)
        self.color_anim.start()

    def my_update(self):
        text = ""
        if self.signal.last_measured_power is not None:
            text+=str(round(self.signal.last_measured_power,2))+"dBm"
        if self.signal.last_measured_loudness is not None:
            text+=" "+str(round(self.signal.last_measured_loudness,2))+"vol"
        self.setText(text)

        if self.signal.state != self.old_state:
            self.old_state = self.signal.state
            self.updateStatus()

    def getBackColor(self):
        return self.palette().color(QtGui.QPalette.Window)

    def setBackColor(self, color):
        self.my_update()
        self.setStyleSheet("* { background: rgb(%d,%d,%d) }" % (color.red(), color.green(), color.blue()))


    backColor = QtCore.Property(QtGui.QColor, getBackColor, setBackColor)