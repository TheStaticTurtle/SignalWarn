import sys
import platform
import typing

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide6.QtCore import (QPropertyAnimation, QSize, Qt)
from PySide6.QtGui import (QColor, QFont, QBrush)
from PySide6.QtWidgets import *

import os.path

from tools.DemodulationType import DemodulationType
from tools.Signal import Signal as RFSignal
from tools.SignalLibrary import SignalLibrary
from tools.SignalManager import SignalManager
from .ressources import style, files
from .widgets.QSignalStatusWidget import QSignalStatusWidget

files.qInitResources()

from .base import Ui_MainWindow

class MainWindow(QMainWindow):
	def __init__(self, signal_libraries: typing.List[SignalLibrary], signal_manager: SignalManager):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.menus = [
			{"title": "Home",       "btn_id": "btn_home",       "btn_icon": "url(:/16x16/icons/16x16/cil-home.png)",  "page": self.ui.page_home},
			{"title": "Add device", "btn_id": "btn_add_device", "btn_icon": "url(:/16x16/icons/16x16/cil-plus.png)",  "page": self.ui.page_add_device},
			{"title": "Scanner",    "btn_id": "btn_widgets",    "btn_icon": "url(:/16x16/icons/16x16/cil-chart.png)", "page": self.ui.page_scanner},
		]

		self.signal_manager = signal_manager
		self.signal_libraries = signal_libraries
		self.signal_libraries.append("Custom")

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

		self.ui.comboBoxAddDeviceType.clear()
		for signal_library in self.signal_libraries:
			if signal_library == "Custom":
				self.ui.comboBoxAddDeviceType.addItem("Custom")
			else:
				self.ui.comboBoxAddDeviceType.addItem(signal_library.NAME)
		self.ui.comboBoxAddDeviceType.currentTextChanged.connect(self.add_device_comboBox_type_select)
		self.ui.comboBox_addDevice_selector_category.currentTextChanged.connect(self.add_device_comboBox_selector_category)
		self.ui.comboBox_addDevice_selector_signal.currentTextChanged.connect(self.add_device_comboBox_selector_signal)
		self.ui.pushButton_addDevice_save.clicked.connect(self.add_device_button_save)

		self.ui.stackedWidget.setCurrentWidget(self.ui.page_addDevice_custom)

		self.ui.comboBox_addDevice_demodulation.currentTextChanged.connect(self.add_device_comboBox_demodulation)
		self.ui.comboBox_addDevice_demodulation.addItems([x.name.capitalize() for x in list(DemodulationType)])
		self.add_device_comboBox_demodulation("Off")

		self.ui.horizontalSlider_addDevice_signalPresentThreshold.valueChanged.connect(lambda x: self.ui.label_addDevice_signalPresentThreshold.setText(str(x)+""))
		self.ui.horizontalSlider_addDevice_volumeThreshold.valueChanged.connect(lambda x: self.ui.label_addDevice_volumeThreshold.setText(str(x)+"%"))
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
				if menu["btn_id"] == "btn_widgets":
					self.scanner_update_table()
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
					self.ui.doubleSpinBox_addDevice_custom_frequency.value(),
					self.ui.doubleSpinBox_addDevice_custom_bandwidth.value(),
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
			self.scanner_update_table()
			self.ui.comboBox_addDevice_demodulation.setCurrentIndex(0)
			self.ui.lineEdit_addDevice_name.setText("")
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_scanner)
			self.select_menu("btn_widgets")
			print(f"Created: %r" % new_signal)


	def scanner_update_table(self):
		data = {
			"Status": [],
			"Name": [],
			"Freq @ Bw": [],
			"Comment": [],
		}

		self.ui.tableWidget.clear()

		self.ui.tableWidget.setHorizontalHeaderLabels(["Status", "Name", "Freq @ Bw", "Comment", "Actions"])
		self.ui.tableWidget.setColumnCount(5)
		self.ui.tableWidget.horizontalHeader().setVisible(True)
		for y, signal in enumerate(self.signal_manager.get_signals()):
			self.ui.tableWidget.setCellWidget(y, 0, QSignalStatusWidget(signal))
			self.ui.tableWidget.setItem(y, 1, QTableWidgetItem(signal.name))
			self.ui.tableWidget.setItem(y, 2, QTableWidgetItem(signal.human_frequency+" @ "+signal.human_bandwidth))
			self.ui.tableWidget.setItem(y, 3, QTableWidgetItem(signal.parent.name if signal.has_parent else "-"))

			pWidget = QWidget()
			btn_delete = QPushButton()
			btn_delete.setText("Delete")
			pLayout = QHBoxLayout(pWidget)
			pLayout.addWidget(btn_delete)
			pLayout.setContentsMargins(0, 0, 0, 0)
			pWidget.setLayout(pLayout)

			btn_delete.clicked.connect(lambda: self.scanner_delete_signal_callback(signal))
			self.ui.tableWidget.setCellWidget(y, 4, pWidget)

		self.ui.tableWidget.resizeColumnsToContents()
		self.ui.tableWidget.resizeRowsToContents()
	def scanner_delete_signal_callback(self, signal):
		self.signal_manager.remove_signal(signal)
		self.scanner_update_table()

class Gui:
	def __init__(self, signal_libraries: typing.List[SignalLibrary], signal_manager: SignalManager):
		self.app = QApplication(sys.argv)
		QtGui.QFontDatabase.addApplicationFont(os.path.dirname(__file__)+"\\ressources\\fonts\\segoeui.ttf")
		QtGui.QFontDatabase.addApplicationFont(os.path.dirname(__file__)+"\\ressources\\fonts\\segoeuib.ttf")
		self.window = MainWindow(signal_libraries, signal_manager)

	def run(self):
		sys.exit(self.app.exec())