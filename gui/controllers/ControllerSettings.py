import typing

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide6.QtCore import (QPropertyAnimation, QSize, Qt)
from PySide6.QtGui import (QColor, QFont, QBrush)
from PySide6.QtWidgets import *

from gui.base import Ui_MainWindow
from gui.ressources import style, files
from gui.widgets.QColorPicker import QColorPicker
from tools.Config import Config
from tools.DemodulationType import DemodulationType
from tools.Signal import Signal as RFSignal, Signal

from tools.SignalLibrary import SignalLibrary
from tools.SignalManager import SignalManager

from gui.controllers.BaseController import BaseController

class ControllerSettings(BaseController):
	def __init__(self, config: Config, window, ui: Ui_MainWindow, signal_libraries: typing.List[SignalLibrary], signal_manager: SignalManager):
		super().__init__(config)
		self.ui = ui
		self.window = window
		self.signal_libraries = signal_libraries
		self.signal_manager = signal_manager

		self.ui.pushButton_import_signals.pressed.connect(self.settings_importexport_import_signals)
		self.ui.pushButton_export_signals.pressed.connect(self.settings_importexport_export_signals)

		self.add_colorpickers_to_hl(self.ui.horizontalLayout_settings_color_signal_absent, "ui.color.signal_absent", "ui.color.signal_absent_faded")
		self.add_colorpickers_to_hl(self.ui.horizontalLayout_settings_color_signal_unknown, "ui.color.signal_unknown", "ui.color.signal_unknown_faded")
		self.add_colorpickers_to_hl(self.ui.horizontalLayout_settings_color_signal_muted, "ui.color.signal_muted", "ui.color.signal_muted_faded")
		self.add_colorpickers_to_hl(self.ui.horizontalLayout_settings_color_signal_normal, "ui.color.signal_normal", "ui.color.signal_normal_faded")
		self.add_colorpickers_to_hl(self.ui.horizontalLayout_settings_color_signal_checking, "ui.color.checking_signal", "ui.color.checking_signal_faded")

	def add_colorpickers_to_hl(self,layout, settingA, settingB):
		colorPicker_A = QColorPicker(QColor(*self.config.get(settingA, (255, 255, 255))))
		colorPicker_B = QColorPicker(QColor(*self.config.get(settingB, (255, 255, 255))))
		colorPicker_A.setMinimumSize(100,15)
		colorPicker_B.setMinimumSize(100,15)
		layout.addWidget(colorPicker_A)
		layout.addWidget(colorPicker_B)

		colorPicker_A.on_color.connect(lambda color: self.config.set(settingA, (color.red(), color.green(), color.blue())))
		colorPicker_B.on_color.connect(lambda color: self.config.set(settingB, (color.red(), color.green(), color.blue())))


	def settings_importexport_import_signals(self):
		self.logger.info("Opening open file dialog")
		filename = QFileDialog.getOpenFileName(self.window, "Open file", "", "*.json")
		if filename[0] != '':
			self.signal_manager.load(filename[0])
			self.window.controller_scanner.update_table()

	def settings_importexport_export_signals(self):
		self.logger.info("Opening save file dialog")
		filename = QFileDialog.getSaveFileName(self.window, "Save file", "", "*.json")
		if filename[0] != '':
			self.signal_manager.save(filename[0])
			self.window.controller_scanner.update_table()