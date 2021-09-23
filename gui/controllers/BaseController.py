import logging
import typing

from PySide6.QtWidgets import QMainWindow

from tools.Config import Config


class BaseController(QMainWindow):
	def __init__(self, config: Config):
		super().__init__()
		self.config = config
		self.logger = logging.getLogger("UI"+self.__class__.__name__)
		self.logger.debug("Hellow, world")