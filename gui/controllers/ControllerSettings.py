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

class ControllerSettings(BaseController):
	def __init__(self, window, ui: Ui_MainWindow, signal_libraries: typing.List[SignalLibrary], signal_manager: SignalManager):
		super().__init__()
		self.ui = ui
		self.window = window
		self.signal_libraries = signal_libraries
		self.signal_manager = signal_manager

		self.ui.pushButton_import_signals.pressed.connect(self.settings_importexport_import_signals)
		self.ui.pushButton_export_signals.pressed.connect(self.settings_importexport_export_signals)



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