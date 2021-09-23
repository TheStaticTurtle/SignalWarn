import logging

import pylab as plt
import numpy as np
import scipy.signal as signal
from radio.analog import MFM
import math

from tools.Config import Config
from tools.DemodulationType import DemodulationType


class BaseSDR:
	def __init__(self, config: Config, debug=False):
		self.config = config
		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.debug("Hellow, world")

		self._check_settle_time = self.config.get("radio.sdr.settle_time", 0.01)
		self._capture_offset = self.config.get("radio.sdr.capture_offset", 250e3)
		self._samples_per_measurement = self.config.get("radio.sdr.samples_per_measurement", 512*1024)

		if debug:
			self._samples_per_measurement = 10 * 1024 * 1024
		self.debug = debug

	@classmethod
	def _plot_spectrogram(cls, samples, sample_rate, frequency, title):
		fig, ax = plt.subplots()
		color_map = plt.get_cmap('viridis')
		A = 1
		x = A * np.sin(2 * np.pi * frequency * np.arange(0, 15, 1.0 / sample_rate))
		value_min = 20 * np.log10(np.max(x)) - 110  # hide anything below -40 dBc
		# color_map.set_under(color='k', alpha=None)

		N_FFT = 256
		pxx, freq, t, cax = ax.specgram(samples / (N_FFT / 2), Fs=sample_rate, mode='magnitude', vmin=value_min, NFFT=N_FFT, noverlap=N_FFT / 2, cmap=color_map, window=plt.window_none)
		fig.colorbar(cax)

		plt.title(title)
		plt.xlim(0, len(samples) / sample_rate)
		plt.xlabel("Time (s)")
		plt.ylabel("Frequency (Hz)")
		plt.ticklabel_format(style='plain', axis='y')
		plt.ylim(-sample_rate / 2, sample_rate / 2)
		fig.show()
	@classmethod
	def _plot_audio(cls, samples, sample_rate, title):
		plt.figure(1)
		plt.title(title)

		plot_a = plt.subplot(211, title=title)
		plot_a.plot(samples)
		plot_a.set_xlabel('SR * T')
		plot_a.set_ylabel('Energy')

		plot_b = plt.subplot(212)
		plot_b.specgram(samples, NFFT=1024, Fs=sample_rate, noverlap=900)
		plot_b.set_xlabel('Time')
		plot_b.set_ylabel('Frequency')

		plt.show()
	@classmethod
	def _plot_npfft(cls, samples, sample_rate, title):
		frequencies = np.fft.fftfreq(samples.size, 1 / sample_rate)
		idx = np.argsort(frequencies)
		ps = np.abs(np.fft.fft(samples)) ** 2

		plt.figure()
		plt.plot(frequencies[idx], ps[idx])
		plt.ylabel("Power")
		plt.xlabel("Frequency (Hz)")
		plt.ylim(0, 100e3)
		plt.title(title)
		plt.show()

	def _process_signal_convert(self, frequency, samples, sample_rate):
		if self.debug:
			self._plot_spectrogram(samples, sample_rate, frequency, "Base signal")
		return samples, sample_rate
	def _process_signal_recenter(self, frequency, samples, sample_rate):
		fc1 = np.exp(-1.0j * 2.0 * np.pi * -self._capture_offset / sample_rate * np.arange(len(samples)))
		samples_offset = samples * fc1
		if self.debug:
			self._plot_spectrogram(samples_offset, sample_rate, frequency, "Offset-ed")
		return samples_offset, sample_rate
	def _process_signal_decimate(self, frequency, samples, sample_rate, filter_bw):
		dec_rate = int(sample_rate / filter_bw)
		samples_decimated = signal.decimate(samples, dec_rate)
		# Calculate the new sampling rate
		sample_rate = sample_rate / dec_rate

		if self.debug:
			self._plot_spectrogram(samples_decimated, sample_rate, frequency, "Decimated")

		return samples_decimated, sample_rate
	def _process_signal_de_emphasis(self, frequency, samples, sample_rate):
		# The de-emphasis filter
		# Given a signal 'x5' (in a numpy array) with sampling rate Fs_y
		d = sample_rate * 75e-6  # Calculate the # of samples to hit the -3dB point
		x = np.exp(-1 / d)  # Calculate the decay between each sample
		b = [1 - x]  # Create the filter coefficients
		a = [1, -x]
		samples_de_emphasis = signal.lfilter(b, a, samples)

		if self.debug:
			self._plot_spectrogram(samples_de_emphasis, sample_rate, frequency, "De-Emphasis")

		return samples_de_emphasis, sample_rate

	def _analyse_signal_power(self, samples, sample_rate):
		if self.debug:
			self._plot_npfft(samples, sample_rate, "Power analysis")

		# Formula is P(dBm) = 10 * LOG( 10 * (I**2 + Q**2))
		sq_samples = np.abs(samples) ** 2
		lg_samples = 10*np.log(10 * sq_samples)
		avg_pwr = np.mean(lg_samples)

		return avg_pwr
	def _analyse_audio_power(self, samples, sample_rate):
		if self.debug:
			self._plot_npfft(samples, sample_rate, "Audio Power analysis")

		return np.linalg.norm(samples)

	def _demodulate_fm(self, frequency, samples, sample_rate):
		samples_decimated, sample_rate_decimated = self._process_signal_decimate(frequency, samples, sample_rate, 100e3)
		tau = 75e-6
		audio_sample_rate = 25e3

		demod = MFM(tau, sample_rate_decimated, audio_sample_rate, cuda=False)
		outdata = demod.run(samples_decimated)
		LPR = outdata.astype(np.float32)

		if self.debug:
			self._plot_audio(outdata, audio_sample_rate, "FM Demodulated audio")

		return LPR, audio_sample_rate

	def pre_read_radio_samples(self, frequency, bandwidth=12.5e3):
		self.logger.info("Reading %d samples at %d @ %d" % (self._samples_per_measurement, frequency, bandwidth))
		return None, 0

	def check_frequency_from_samples(self, samples, sample_rate, frequency, bandwidth=12.5e3, min_power=-math.inf, enable_de_emphasis=False, demodulate=DemodulationType.OFF, min_loudness=0):
		bandwidth_mini = self.config.get("radio.processing.minimum_filter_bw", 100e3)
		bandwidth = bandwidth_mini if bandwidth < bandwidth_mini else bandwidth*2

		samples, sample_rate = self._process_signal_convert(frequency, samples, sample_rate)
		samples, sample_rate = self._process_signal_recenter(frequency, samples, sample_rate)
		samples, sample_rate = self._process_signal_decimate(frequency, samples, sample_rate, bandwidth)

		if enable_de_emphasis:
			samples, sample_rate = self._process_signal_de_emphasis(frequency, samples, sample_rate)

		avg_power = self._analyse_signal_power(samples, sample_rate)

		if demodulate == DemodulationType.OFF:
			return avg_power > min_power, avg_power, None, None

		samples_audio, sample_rate_audio = None, None
		if demodulate == DemodulationType.FM:
			samples_audio, sample_rate_audio = self._demodulate_fm(frequency, samples, sample_rate)

		avg_loudness = self._analyse_audio_power(samples_audio, sample_rate_audio)

		self.logger.info("Signal analysis finished: present=%r avg_power=%f audio_present=%r, loudness=%f" % (avg_power > min_power, avg_power, avg_loudness > min_loudness, avg_loudness))
		return avg_power > min_power, avg_power, avg_loudness > min_loudness, avg_loudness

	def check_frequency(self, frequency, bandwidth=12.5e3, min_power=-math.inf, enable_de_emphasis=False, demodulate=DemodulationType.OFF, min_loudness=0):
		samples, sample_rate = self.pre_read_radio_samples(frequency, bandwidth)
		return self.check_frequency_from_samples(samples, sample_rate, frequency, bandwidth, min_power, enable_de_emphasis, demodulate, min_loudness)
