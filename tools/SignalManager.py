from . import Signal


class SignalManager:
	NAME = "GenericSignalLibrary"

	def __init__(self):
		self.signals = []

	def add_signal(self, signal: Signal) -> bool:
		self.signals.append(signal)
		return True

	def remove_signal(self, signal: Signal) -> bool:
		if signal in self.signals:
			self.signals.remove(signal)
			return True
		return False

	def get_signals(self):
		return self.signals

