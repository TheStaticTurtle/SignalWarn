import typing

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide6.QtCore import (QPropertyAnimation, QSize, Qt)
from PySide6.QtGui import (QColor, QFont, QBrush)
from PySide6.QtWidgets import *

from ..base import Ui_MainWindow
from ..ressources import style, files
from tools.DemodulationType import DemodulationType
from tools.Signal import Signal as RFSignal, Signal

from tools.SignalLibrary import SignalLibrary
from tools.SignalManager import SignalManager

from ..widgets.QSignalCheckedWidget import QSignalCheckedWidget
from ..widgets.QSignalStatusWidget import QSignalStatusWidget

from .BaseController import BaseController

class ControllerScanner(BaseController):
	def __init__(self, parent, ui: Ui_MainWindow, signal_libraries: typing.List[SignalLibrary], signal_manager: SignalManager):
		super().__init__()
		self.ui = ui
		self.parent = parent
		self.signal_libraries = signal_libraries
		self.signal_manager = signal_manager

		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)


	def scanner_update_table(self):
		data = {
			"Status": [],
			"Name": [],
			"Freq @ Bw": [],
			"Comment": [],
		}

		self.ui.tableWidget.clear()

		self.ui.tableWidget.setHorizontalHeaderLabels(["", "Status", "Name", "Freq @ Bw", "Comment", "Actions"])
		self.ui.tableWidget.setColumnCount(6)
		self.ui.tableWidget.setRowCount(len(self.signal_manager.get_signals())+1)
		self.ui.tableWidget.horizontalHeader().setVisible(True)
		for y, signal in enumerate(self.signal_manager.get_signals()):
			self.ui.tableWidget.setCellWidget(y, 0, QSignalCheckedWidget(signal))
			self.ui.tableWidget.setCellWidget(y, 1, QSignalStatusWidget(signal))
			self.ui.tableWidget.setItem(y, 2, QTableWidgetItem(signal.name))
			self.ui.tableWidget.setItem(y, 3, QTableWidgetItem(signal.human_frequency+" @ "+signal.human_bandwidth))
			self.ui.tableWidget.setItem(y, 4, QTableWidgetItem(signal.parent.name if signal.has_parent else "-"))

			pWidget = QWidget()
			btn_delete = QPushButton()
			btn_delete.setText("Delete")
			pLayout = QHBoxLayout(pWidget)
			pLayout.addWidget(btn_delete)
			pLayout.setContentsMargins(0, 0, 0, 0)
			pWidget.setLayout(pLayout)

			def delete_sig_callback(s: Signal):
				def _():
					print("Deleting %r" % s)
					self.scanner_delete_signal_callback(s)
				return _
			btn_delete.clicked.connect(delete_sig_callback(signal))
			self.ui.tableWidget.setCellWidget(y, 5, pWidget)

		self.ui.tableWidget.resizeColumnsToContents()
		self.ui.tableWidget.resizeRowsToContents()
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
		self.ui.stackedWidget.setCurrentWidget(self.ui.page_scanner)

		self.parent.controller_menu.select_menu("btn_scanner")

	def scanner_delete_signal_callback(self, signal):
		self.signal_manager.remove_signal(signal)
		self.scanner_update_table()