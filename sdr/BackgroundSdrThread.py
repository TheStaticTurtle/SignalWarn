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
				signal.is_been_checked = True
				present, power, audio_present, audio_loudness = self.sdr.check_frequency(
					signal.frequency,
					bandwidth=signal.bandwidth,
					min_power=signal.threshold_signal,
					enable_de_emphasis=False,
					demodulate=signal.demodulation,
					min_loudness=signal.threshold_volume
				)
				signal.set_last_measured_power(power)
				signal.set_last_measured_audio_loudness(audio_loudness)
				signal.set_present(present, audio_present)
				signal.is_been_checked = False
