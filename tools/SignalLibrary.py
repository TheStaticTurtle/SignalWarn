from . import Signal


class SignalLibrary:
	NAME = "GenericSignalLibrary"

	def __init__(self):
		self.signals = {
			"CategoryA": [],
			"CategoryB": []
		}

	def get_all_signals(self):
		out = []
		for cat in self.signals.keys():
			out += self.signals[cat]
		return out

	def get_signals_in_category(self, cat):
		if cat not in self.signals.keys():
			return []
		return self.signals[cat]

	def get_categories(self):
		return [str(x) for x in self.signals.keys()]

