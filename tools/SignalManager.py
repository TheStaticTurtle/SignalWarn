import json
import typing

from .Signal import Signal


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

	def get_signals(self) -> typing.List[Signal]:
		return self.signals

	def load(self, filename):
		data = json.loads(open(filename,"r").read())
		self.signals = []
		for dict_signal in data["signals"]:
			self.add_signal(Signal.from_dict(dict_signal))

	def save(self, filename):
		data = {
			"signals": [signal.to_dict() for signal in self.signals]
		}
		open(filename, "w").write(json.dumps(data))

