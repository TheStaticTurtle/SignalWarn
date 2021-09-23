import threading

from sdr.BaseSDR import BaseSDR
from tools.Signal import Signal
from tools.SignalManager import SignalManager

class BackgroundCheckProcessThread(threading.Thread):
	def __init__(self, sdr: BaseSDR, data, signal: Signal):
		super().__init__()
		self.sdr = sdr
		self.data = data
		self.signal = signal

	def run(self):
		self.signal.is_been_checked = True
		present, power, audio_present, audio_loudness = self.sdr.check_frequency_from_samples(*self.data,
		                                                                                      self.signal.frequency,
		                                                                                      bandwidth=self.signal.bandwidth,
		                                                                                      min_power=self.signal.threshold_signal,
		                                                                                      enable_de_emphasis=False,
		                                                                                      demodulate=self.signal.demodulation,
		                                                                                      min_loudness=self.signal.threshold_volume
		                                                                                      )
		self.signal.set_last_measured_power(power)
		self.signal.set_last_measured_audio_loudness(audio_loudness)
		self.signal.set_present(present, audio_present)
		self.signal.is_been_checked = False

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
				data = self.sdr.pre_read_radio_samples(signal.frequency, bandwidth=signal.bandwidth)
				t = BackgroundCheckProcessThread(self.sdr, data, signal)
				t.start()
