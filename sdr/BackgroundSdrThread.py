import threading

from sdr.BaseSDR import BaseSDR
from tools.SignalManager import SignalManager


class BackgroundSdrThread(threading.Thread):
	def __init__(self, sdr: BaseSDR, signals_manager: SignalManager):
		super().__init__()
		self.running = True
		self.signals_manager = signals_manager
		self.sdr = sdr

	def quit(self):
		self.running = False

	def run(self):
		while self.running:
			for signal in self.signals_manager.get_signals():
				present, power = self.sdr.check_frequency(signal.frequency, bandwidth=signal.bandwidth, min_power=signal.threshold_signal, enable_de_emphasis=False)
				signal.set_last_measured_power(power)
				signal.set_present(present)
				pass
