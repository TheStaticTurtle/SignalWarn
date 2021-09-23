import json
import logging
import typing

from .Signal import Signal


class SignalManager:
	NAME = "GenericSignalLibrary"

	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.debug("Hellow, world")
		self.signals = []

	def add_signal(self, signal: Signal) -> bool:
		self.signals.append(signal)
		self.logger.info("Added signal: %r" % signal)
		return True

	def remove_signal(self, signal: Signal) -> bool:
		if signal in self.signals:
			self.signals.remove(signal)
			self.logger.info("Removed signal: %r" % signal)
			return True
		self.logger.warning("Could not remove signal (not present): %r" % signal)
		return False

	def clear_all(self) -> bool:
		self.signals.clear()
		self.logger.info("Cleared all signals")
		return True

	def get_signals(self) -> typing.List[Signal]:
		return self.signals

	def load(self, filename):
		data = json.loads(open(filename,"r").read())
		self.signals = []
		for dict_signal in data["signals"]:
			self.add_signal(Signal.from_dict(dict_signal))
		self.logger.info("Successfully loaded signals from file")

	def save(self, filename):
		data = {
			"signals": [signal.to_dict() for signal in self.signals]
		}
		open(filename, "w").write(json.dumps(data))
		self.logger.info("Successfully saved current signals")
