import pylab as plt
import numpy as np
import scipy.signal as signal




class BaseSDR:
	def __init__(self, check_settle_time=0.01, debug=False):
		self._check_settle_time = check_settle_time
		self._capture_offset = 250e3
		self._samples_per_measurement = 256 * 1024
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


	def _analyse_signal_get_power(self, samples, sample_rate):
		if self.debug:
			frequencies = np.fft.fftfreq(samples.size, 1 / sample_rate)
			idx = np.argsort(frequencies)
			ps = np.abs(np.fft.fft(samples)) ** 2

			plt.figure()
			plt.plot(frequencies[idx], ps[idx])
			plt.ylabel("Power")
			plt.xlabel("Frequency (Hz)")
			plt.ylim(0, 100e3)
			plt.title('Power spectrum (np.fft.fft)')
			plt.show()

		# Formula is P(dBm) = 10 * LOG( 10 * (I**2 + Q**2))
		sq_samples = np.abs(samples) ** 2
		lg_samples = 10*np.log(10 * sq_samples)
		avg_pwr = np.mean(lg_samples)

		return avg_pwr


	def check_frequency(self, frequency, bandwidth=12.5e3, min_power=0, enable_de_emphasis=False):
		return False, 0
