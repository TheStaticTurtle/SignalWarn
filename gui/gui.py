import sys
import platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QPropertyAnimation, QSize, Qt)
from PySide6.QtGui import (QColor, QFont)
from PySide6.QtWidgets import *

import os.path

from .ressources import style, files
files.qInitResources()

from .base import Ui_MainWindow


class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.menus = [
			{"title": "Home",       "btn_id": "btn_home",       "btn_icon": "url(:/16x16/icons/16x16/cil-home.png)",  "page": self.ui.page_home},
			{"title": "Add device", "btn_id": "btn_add_device", "btn_icon": "url(:/16x16/icons/16x16/cil-plus.png)",  "page": self.ui.page_add_device},
			{"title": "Scanner",    "btn_id": "btn_widgets",    "btn_icon": "url(:/16x16/icons/16x16/cil-chart.png)", "page": self.ui.page_scanner},
		]

		print('System: ' + platform.system())
		print('Version: ' + platform.release())

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

		self.ui.btn_toggle_menu.clicked.connect(lambda: self.toggle_menu(220))

		self.ui.stackedWidget.setMinimumWidth(20)
		for menu in self.menus:
			self.add_menu_button(menu["title"], menu["btn_id"], menu["btn_icon"])

		self.select_menu(self.menus[0]["btn_id"])
		self.ui.stackedWidget.setCurrentWidget(self.menus[0]["page"])


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

		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
		self.show()

	def toggle_menu(self, maxWidth):
		width = self.ui.frame_left_menu.width()
		maxExtend = maxWidth

		widthExtended = maxExtend if width == 70 else 70

		self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
		self.animation.setDuration(300)
		self.animation.setStartValue(width)
		self.animation.setEndValue(widthExtended)
		self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
		self.animation.start()


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

	def add_menu_button(self, name, objName, icon):
		font = QFont()
		font.setFamily(u"Segoe UI")
		button = QPushButton(name, self)
		button.setObjectName(objName)
		sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
		sizePolicy3.setHorizontalStretch(0)
		sizePolicy3.setVerticalStretch(0)
		sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
		button.setSizePolicy(sizePolicy3)
		button.setMinimumSize(QSize(0, 70))
		button.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
		button.setFont(font)
		button.setStyleSheet(style.style_bt_standard.replace('ICON_REPLACE', icon))
		button.setText(name)
		button.setToolTip(name)
		button.clicked.connect(self.menu_buttons_callback)
		self.ui.layout_menus.addWidget(button)

	def menu_buttons_callback(self):
		btnWidget = self.sender()
		for menu in self.menus:
			if menu["btn_id"] == btnWidget.objectName():
				self.ui.stackedWidget.setCurrentWidget(menu["page"])
				self.select_menu(menu["btn_id"])

	def select_menu(self, widget):
		for w in self.ui.frame_left_menu.findChildren(QPushButton):
			style = w.styleSheet()
			if w.objectName() == widget:
				style += "QPushButton { border-right: 7px solid rgb(44, 49, 60); }"
			else:
				style = style.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
			w.setStyleSheet(style)

	def mousePressEvent(self, event):
		self.dragPos = event.globalPos()


class Gui:
	def __init__(self):
		self.app = QApplication(sys.argv)
		QtGui.QFontDatabase.addApplicationFont(os.path.dirname(__file__)+"\\ressources\\fonts\\segoeui.ttf")
		QtGui.QFontDatabase.addApplicationFont(os.path.dirname(__file__)+"\\ressources\\fonts\\segoeuib.ttf")
		self.window = MainWindow()

	def run(self):
		sys.exit(self.app.exec())
