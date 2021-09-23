import sys
import typing

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide6.QtWidgets import *

import os.path

from tools.Config import Config
from tools.SignalLibrary import SignalLibrary
from tools.SignalManager import SignalManager
from gui.controllers.ControllerAddSignal import ControllerAddSignal
from gui.controllers.ControllerMenus import ControllerMenu
from gui.controllers.ControllerScanner import ControllerScanner
from gui.controllers.ControllerSettings import ControllerSettings

from gui.gui_mainwindow import MainWindow


from gui.ressources import style, files
files.qInitResources()

class Gui:
	def __init__(self, confg: Config, signal_libraries: typing.List[SignalLibrary], signal_manager: SignalManager):
		self.config = confg
		self.app = QApplication(sys.argv)
		QtGui.QFontDatabase.addApplicationFont(os.path.dirname(__file__)+"\\ressources\\fonts\\segoeui.ttf")
		QtGui.QFontDatabase.addApplicationFont(os.path.dirname(__file__)+"\\ressources\\fonts\\segoeuib.ttf")

		self.signal_manager = signal_manager
		self.signal_libraries = signal_libraries
		self.signal_libraries.append("Custom")

		self.window = MainWindow()

		self.window.controller_menu = ControllerMenu(self.config, self.window, self.window.ui, self.signal_libraries, self.signal_manager)
		self.window.controller_add_signal = ControllerAddSignal(self.config, self.window, self.window.ui, self.signal_libraries, self.signal_manager)
		self.window.controller_scanner = ControllerScanner(self.config, self.window, self.window.ui, self.signal_libraries, self.signal_manager)
		self.window.controller_settings = ControllerSettings(self.config, self.window, self.window.ui, self.signal_libraries, self.signal_manager)

		self.window.controller_scanner.update_table()
		self.window.show()

	def run(self):
		self.app.exec()