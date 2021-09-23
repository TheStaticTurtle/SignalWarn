import typing

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide6.QtCore import (QPropertyAnimation, QSize, Qt)
from PySide6.QtGui import (QColor, QFont, QBrush)
from PySide6.QtWidgets import *

from gui.base import Ui_MainWindow
from gui.ressources import style, files
from tools.DemodulationType import DemodulationType
from tools.Signal import Signal as RFSignal, Signal

from tools.SignalLibrary import SignalLibrary
from tools.SignalManager import SignalManager

from gui.controllers.BaseController import BaseController

class ControllerMenu(BaseController):
	def __init__(self, window, ui: Ui_MainWindow, signal_libraries: typing.List[SignalLibrary], signal_manager: SignalManager):
		super().__init__()
		self.ui = ui
		self.window = window
		self.signal_libraries = signal_libraries
		self.signal_manager = signal_manager

		self.menus = [
			{"title": "Home", "btn_id": "btn_home", "btn_icon": "url(:/16x16/icons/16x16/cil-home.png)",  "page": self.ui.page_home},
			{"title": "Scanner", "btn_id": "btn_scanner", "btn_icon": "url(:/16x16/icons/16x16/cil-chart.png)", "page": self.ui.page_scanner},
			{"title": "Add device", "btn_id": "btn_add_device", "btn_icon": "url(:/16x16/icons/16x16/cil-plus.png)", "page": self.ui.page_add_device},
			{"title": "Settings", "btn_id": "btn_settings", "btn_icon": "url(:/16x16/icons/16x16/cil-settings.png)", "page": self.ui.page_settings},
		]

		self.ui.btn_toggle_menu.clicked.connect(lambda: self.toggle_menu(220))

		self.ui.stackedWidget.setMinimumWidth(20)
		for menu in self.menus:
			self.add_menu_button(menu["title"], menu["btn_id"], menu["btn_icon"])
			self.logger.debug("Created menu %s with id %s" % (menu["title"], menu["btn_id"]))
		self.logger.info("Added %d menus" % len(self.menus))

		self.select_menu(self.menus[0]["btn_id"])
		self.ui.stackedWidget.setCurrentWidget(self.menus[0]["page"])


	def toggle_menu(self, maxWidth):
		self.logger.debug("Toggling sidebar menu")
		width = self.ui.frame_left_menu.width()
		maxExtend = maxWidth

		widthExtended = maxExtend if width == 70 else 70

		self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
		self.animation.setDuration(300)
		self.animation.setStartValue(width)
		self.animation.setEndValue(widthExtended)
		self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
		self.animation.start()


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
				if menu["btn_id"] == "btn_scanner":
					self.window.controller_scanner.update_table()
				self.ui.stackedWidget.setCurrentWidget(menu["page"])
				self.window.controller_menu.select_menu(menu["btn_id"])
				self.logger.info("Button %s clicked opening %r" % (menu["btn_id"], menu["page"]))

	def select_menu(self, widget):
		for w in self.ui.frame_left_menu.findChildren(QPushButton):
			css = w.styleSheet()
			if w.objectName() == widget:
				css += "QPushButton { border-right: 7px solid rgb(44, 49, 60); }"
			else:
				css = css.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
			w.setStyleSheet(css)
