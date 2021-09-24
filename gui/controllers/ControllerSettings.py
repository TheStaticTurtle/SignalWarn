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

		self.ui.checkBox_rf_settings_processing_de_emphasis.setChecked(self.config.get("radio.processing.enable_de_emphasis", False))
		self.ui.checkBox_rf_settings_processing_de_emphasis.stateChanged.connect(lambda: self.config.set("radio.processing.enable_de_emphasis", self.ui.checkBox_rf_settings_processing_de_emphasis.isChecked()))

		self.ui.spinBox_rf_settings_processing_min_filter_bandwidth.setValue(int(self.config.get("radio.processing.minimum_filter_bw", 100000.0)))
		self.ui.spinBox_rf_settings_processing_min_filter_bandwidth.valueChanged.connect(lambda: self.config.set("radio.processing.minimum_filter_bw", self.ui.spinBox_rf_settings_processing_min_filter_bandwidth.value()))

		self.ui.spinBox_rf_settings_sdr_sample_per_measurment.setValue(int(self.config.get("radio.sdr.samples_per_measurement", 512*1024)))
		self.ui.spinBox_rf_settings_sdr_sample_per_measurment.valueChanged.connect(lambda: self.config.set("radio.sdr.samples_per_measurement", self.ui.spinBox_rf_settings_sdr_sample_per_measurment.value()))

		self.ui.spinBox_rf_settings_sdr_capture_offset.setValue(int(self.config.get("radio.sdr.capture_offset", 250000.0)))
		self.ui.spinBox_rf_settings_sdr_capture_offset.valueChanged.connect(lambda: self.config.set("radio.sdr.capture_offset", self.ui.spinBox_rf_settings_sdr_capture_offset.value()))

		self.ui.spinBox_rf_settings_sdr_sample_rate.setValue(int(self.config.get("radio.sdr.sample_rate", 2400000.0)))
		self.ui.spinBox_rf_settings_sdr_sample_rate.valueChanged.connect(lambda: self.config.set("radio.sdr.sample_rate", self.ui.spinBox_rf_settings_sdr_sample_rate.value()))

		self.ui.doubleSpinBox_rf_settings_sdr_settle_time.setValue(self.config.get("radio.sdr.settle_time", 0.01))
		self.ui.doubleSpinBox_rf_settings_sdr_settle_time.valueChanged.connect(lambda: self.config.set("radio.sdr.settle_time", self.ui.doubleSpinBox_rf_settings_sdr_settle_time.value()))


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