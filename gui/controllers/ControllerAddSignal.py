import typing

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide6.QtCore import (QPropertyAnimation, QSize, Qt)
from PySide6.QtGui import (QColor, QFont, QBrush)
from PySide6.QtWidgets import *

from tools.DemodulationType import DemodulationType
from tools.Signal import Signal as RFSignal, Signal

from tools.SignalLibrary import SignalLibrary
from tools.SignalManager import SignalManager

from .BaseController import BaseController
from ..base import Ui_MainWindow


class ControllerAddSignal(BaseController):
	def __init__(self, parent, ui: Ui_MainWindow, signal_libraries: typing.List[SignalLibrary], signal_manager: SignalManager):
		super().__init__()
		self.ui = ui
		self.parent = parent
		self.signal_libraries = signal_libraries
		self.signal_manager = signal_manager

		self.ui.comboBoxAddDeviceType.clear()
		for signal_library in self.signal_libraries:
			if signal_library == "Custom":
				self.ui.comboBoxAddDeviceType.addItem("Custom")
			else:
				self.ui.comboBoxAddDeviceType.addItem(signal_library.NAME)
		self.ui.comboBoxAddDeviceType.currentTextChanged.connect(self.add_device_comboBox_type_select)
		self.ui.comboBox_addDevice_selector_category.currentTextChanged.connect(
			self.add_device_comboBox_selector_category)
		self.ui.comboBox_addDevice_selector_signal.currentTextChanged.connect(self.add_device_comboBox_selector_signal)
		self.ui.pushButton_addDevice_save.clicked.connect(self.add_device_button_save)

		self.ui.stackedWidget.setCurrentWidget(self.ui.page_addDevice_custom)

		self.ui.comboBox_addDevice_demodulation.currentTextChanged.connect(self.add_device_comboBox_demodulation)
		self.ui.comboBox_addDevice_demodulation.addItems([x.name.capitalize() for x in list(DemodulationType)])
		self.add_device_comboBox_demodulation("Off")

		self.ui.horizontalSlider_addDevice_signalPresentThreshold.valueChanged.connect(
			lambda x: self.ui.label_addDevice_signalPresentThreshold.setText(str(x) + "dBm"))
		self.ui.horizontalSlider_addDevice_volumeThreshold.valueChanged.connect(
			lambda x: self.ui.label_addDevice_volumeThreshold.setText(str(x) + "%"))


	def add_device_comboBox_type_select(self, value):
		if value == "Custom":
			self.ui.stackedWidget_Add_Device.setCurrentWidget(self.ui.page_addDevice_custom)
		else:
			self.ui.stackedWidget_Add_Device.setCurrentWidget(self.ui.page_addDevice_selector)
			library = [l for l in self.signal_libraries if l != "Custom" and l.NAME == value][0]
			self.ui.comboBox_addDevice_selector_category.clear()
			self.ui.comboBox_addDevice_selector_signal.clear()

			cats = library.get_categories()
			self.ui.comboBox_addDevice_selector_category.addItems(cats)

	def add_device_comboBox_selector_category(self, value):
		library = [l for l in self.signal_libraries if l != "Custom" and l.NAME == self.ui.comboBoxAddDeviceType.currentText()]
		if len(library) > 0:
			library = library[0]

			signals = library.get_signals_in_category(value)
			self.ui.comboBox_addDevice_selector_signal.clear()
			self.ui.comboBox_addDevice_selector_signal.addItems([sig.human_id for sig in signals])
		else:
			print("Could find library")

	def add_device_comboBox_selector_signal(self, value):
		library = [l for l in self.signal_libraries if l != "Custom" and l.NAME == self.ui.comboBoxAddDeviceType.currentText()]
		if len(library) > 0:
			library = library[0]

			signals = library.get_signals_in_category(self.ui.comboBox_addDevice_selector_category.currentText())
			signal = [s for s in signals if s.human_id == value]
			if len(signal) > 0:
				signal = signal[0]
				self.ui.label_addDevice_selector_frequency.setText(signal.human_frequency)
				self.ui.label_addDevice_selector_bandwidth.setText(signal.human_bandwidth)

				if signal.demodulation is not None:
					index = self.ui.comboBox_addDevice_demodulation.findText(signal.demodulation.name.capitalize(), QtCore.Qt.MatchFixedString)
					if index >= 0:
						self.ui.comboBox_addDevice_demodulation.setCurrentIndex(index)
			else:
				print("Could find signal")
		else:
			print("Could find library")

	def add_device_comboBox_demodulation(self, value):
		if value == "Off":
			self.ui.label_addDevice_volumeThreshold_title.setVisible(False)
			self.ui.label_addDevice_volumeThreshold.setVisible(False)
			self.ui.horizontalSlider_addDevice_volumeThreshold.setVisible(False)
		else:
			self.ui.label_addDevice_volumeThreshold_title.setVisible(True)
			self.ui.label_addDevice_volumeThreshold.setVisible(True)
			self.ui.horizontalSlider_addDevice_volumeThreshold.setVisible(True)

	def add_device_button_save(self):
		new_signal = None

		if self.ui.lineEdit_addDevice_name.text() != "":
			demod = [x for x in list(DemodulationType) if x.name.capitalize() == self.ui.comboBox_addDevice_demodulation.currentText()][0]

			if self.ui.comboBoxAddDeviceType.currentText() == "Custom":
				new_signal = RFSignal(
					self.ui.lineEdit_addDevice_name.text(),
					self.ui.doubleSpinBox_addDevice_custom_frequency.value()*1e6,
					self.ui.doubleSpinBox_addDevice_custom_bandwidth.value()*1e3,
					demodulation=demod,
					threshold_signal=self.ui.horizontalSlider_addDevice_signalPresentThreshold.value(),
					threshold_volume=None if demod == DemodulationType.OFF else self.ui.horizontalSlider_addDevice_volumeThreshold.value(),
				)
			else:
				library = [l for l in self.signal_libraries if l != "Custom" and l.NAME == self.ui.comboBoxAddDeviceType.currentText()]
				if len(library) > 0:
					library = library[0]

					signals = library.get_signals_in_category(self.ui.comboBox_addDevice_selector_category.currentText())
					signal = [s for s in signals if s.human_id == self.ui.comboBox_addDevice_selector_signal.currentText()]
					if len(signal) > 0:
						signal = signal[0]
						self.ui.label_addDevice_selector_frequency.setText(signal.human_frequency)
						self.ui.label_addDevice_selector_bandwidth.setText(signal.human_bandwidth)

						new_signal = RFSignal(
							self.ui.lineEdit_addDevice_name.text(),
							signal.frequency,
							signal.bandwidth,
							demodulation=demod,
							threshold_signal=self.ui.horizontalSlider_addDevice_signalPresentThreshold.value(),
							threshold_volume=None if demod == DemodulationType.OFF else self.ui.horizontalSlider_addDevice_volumeThreshold.value(),

							parent=signal
						)
					else:
						print("Could find signal")
				else:
					print("Could find library")
		else:
			print("Empty name")

		if new_signal:
			self.signal_manager.add_signal(new_signal)
			self.parent.controller_scanner.scanner_update_table()
			self.ui.comboBox_addDevice_demodulation.setCurrentIndex(0)
			self.ui.lineEdit_addDevice_name.setText("")
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_scanner)
			self.parent.controller_menu.select_menu("btn_scanner")
			print(f"Created: %r" % new_signal)