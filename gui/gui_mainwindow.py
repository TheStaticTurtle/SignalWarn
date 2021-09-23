import platform
import typing

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide6.QtCore import (QPropertyAnimation, QSize, Qt)
from PySide6.QtGui import (QColor, QFont, QBrush)
from PySide6.QtWidgets import *

from gui.controllers.ControllerAddSignal import ControllerAddSignal
from gui.controllers.ControllerMenus import ControllerMenu
from gui.controllers.ControllerScanner import ControllerScanner
from gui.controllers.ControllerSettings import ControllerSettings
from gui.ressources import style, files

files.qInitResources()

from gui.base import Ui_MainWindow

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		print('System: ' + platform.system())
		print('Version: ' + platform.release())

		self.controller_menu: typing.Union[ControllerMenu, None]
		self.controller_add_signal: typing.Union[ControllerAddSignal, None]
		self.controller_scanner: typing.Union[ControllerScanner, None]
		self.controller_settings: typing.Union[ControllerSettings, None]

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# Frameless window
		self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
		# self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		def doubleClickMaximizeRestore(event):
			if event.type() == QtCore.QEvent.MouseButtonDblClick:
				QtCore.QTimer.singleShot(250, lambda: self.maximize_restore())
		self.ui.frame_label_top_btns.mouseDoubleClickEvent = doubleClickMaximizeRestore

		self.setWindowTitle('SignalWarn')

		self.resize(QSize(1000, 720))
		self.setMinimumSize(QSize(720, 480))



		self.dragPos = None
		def move_window(event):
			if self.isMaximized():
				self.maximize_restore()
			if event.buttons() == Qt.LeftButton:
				self.move(self.pos() + event.globalPos() - self.dragPos)
				self.dragPos = event.globalPos()
				event.accept()
		self.ui.frame_label_top_btns.mouseMoveEvent = move_window

		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(17)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(QColor(0, 0, 0, 150))
		self.ui.frame_main.setGraphicsEffect(self.shadow)

		self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
		self.ui.btn_maximize_restore.clicked.connect(lambda: self.maximize_restore())
		self.ui.btn_close.clicked.connect(lambda: self.close())

		self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
		self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")


	def maximize_restore(self):
		if not self.isMaximized():
			self.showMaximized()
			self.ui.btn_maximize_restore.setToolTip("Restore")
			self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
			self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
			self.ui.frame_size_grip.hide()
		else:
			self.showNormal()
			self.resize(1000, 720)
			self.ui.btn_maximize_restore.setToolTip("Maximize")
			self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))
			self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
			self.ui.frame_size_grip.show()


	def mousePressEvent(self, event):
		self.dragPos = event.globalPos()