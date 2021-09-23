import os
import select
import threading

from .BaseSDR import BaseSDR
from rtlsdr import *
import numpy as np
import time
from tools.StdoutLoggingCapture import StdoutLoggingCapture


class RtlSDR(BaseSDR):
	def __init__(self, config, gain=12, **kwargs):
		super().__init__(config, **kwargs)

		with StdoutLoggingCapture("RTLSdrCore") as capture:
			self._sdr = RtlSdr()

		self._sdr.sample_rate = self.config.get("radio.sdr.sample_rate", 2.4e6)
		self._sdr.center_freq = 95e6
		self._sdr.gain = gain

	def _process_signal_convert(self, frequency, samples, sample_rate):
		samples = np.array(samples).astype("complex64")

		if self.debug:
			self._plot_spectrogram(samples, sample_rate, frequency, "Base signal")
		return samples, sample_rate

	def pre_read_radio_samples(self, frequency, bandwidth=12.5e3):
		bandwidth_mini = self.config.get("radio.processing.minimum_filter_bw", 100e3)
		bandwidth = bandwidth_mini if bandwidth < bandwidth_mini else bandwidth*2
		self.logger.info("Reading %d samples at %d @ %d" % (self._samples_per_measurement, frequency, bandwidth))

		self._sdr.center_freq = frequency + self._capture_offset
		time.sleep(self._check_settle_time)

		sample_rate = self._sdr.sample_rate
		samples = self._sdr.read_samples(self._samples_per_measurement)
		return samples, sample_rate
