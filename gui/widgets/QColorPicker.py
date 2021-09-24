from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor


class QColorPicker(QtWidgets.QLabel):
	on_color = Signal(QColor)

	def __init__(self, color):
		super(QColorPicker, self).__init__()
		self.setAutoFillBackground(True)
		self._update_color(color)

	def _update_color(self, color):
		self.setStyleSheet("* { background: rgb(%d,%d,%d) }" % (color.red(), color.green(), color.blue()))

	def mousePressEvent(self, event):
		color = QtWidgets.QColorDialog.getColor()
		if color.isValid():
			self._update_color(color)
			self.on_color.emit(color)
