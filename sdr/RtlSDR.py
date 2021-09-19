
from .BaseSDR import BaseSDR
from rtlsdr import *
import numpy as np
import time
import math

class RtlSDR(BaseSDR):
	def __init__(self, gain=12, **kwargs):
		super().__init__(**kwargs)
		self._sdr = RtlSdr()
		self._sdr.sample_rate = 2.4e6
		self._sdr.center_freq = 95e6
		self._sdr.gain = gain

	def _process_signal_convert(self, frequency, samples, sample_rate):
		samples = np.array(samples).astype("complex64")

		if self.debug:
			self._plot_spectrogram(samples, sample_rate, frequency, "Base signal")
		return samples, sample_rate

	def check_frequency(self, frequency, bandwidth=12.5e3, min_power=-math.inf, enable_de_emphasis=False):
		if bandwidth < 100e3:
			bandwidth = 100e3
		else:
			bandwidth = bandwidth*2

		self._sdr.center_freq = frequency + self._capture_offset
		time.sleep(self._check_settle_time)

		sample_rate = self._sdr.sample_rate
		samples = self._sdr.read_samples(self._samples_per_measurement)

		samples, sample_rate = self._process_signal_convert(frequency, samples, sample_rate)
		samples, sample_rate = self._process_signal_recenter(frequency, samples, sample_rate)
		samples, sample_rate = self._process_signal_decimate(frequency, samples, sample_rate, bandwidth)

		if enable_de_emphasis:
			samples, sample_rate = self._process_signal_de_emphasis(frequency, samples, sample_rate)

		avg_power = self._analyse_signal_get_power(samples, sample_rate)

		return avg_power > min_power, avg_power
