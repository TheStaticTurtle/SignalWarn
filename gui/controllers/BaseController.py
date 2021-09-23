import logging
import typing

from PySide6.QtWidgets import QMainWindow

class BaseController(QMainWindow):
	def __init__(self):
		super().__init__()
		self.logger = logging.getLogger("UI"+self.__class__.__name__)
		self.logger.debug("Hellow, world")