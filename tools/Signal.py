import time
from enum import Enum
from si_prefix import si_format

from tools.DemodulationType import DemodulationType


class SignalState(Enum):
	UNKNOWN = 0,
	NORMAL = 1,
	MUTED = 2,
	ABSENT = 3,


class Signal:
	def __init__(self, name: str, frequency: float, bandwidth: float, threshold_signal:float = None, demodulation: DemodulationType = None, threshold_volume: float = None, parent=None):
		self.name = name
		self.frequency = frequency
		self.bandwidth = bandwidth
		self.demodulation = demodulation
		self.threshold_signal = threshold_signal
		self.demodulation = demodulation
		self.threshold_volume = threshold_volume
		self.parent = parent
		self.state = SignalState.UNKNOWN

		self.is_been_checked = False

		self.last_measured_power = None
		self.last_measured_power_time = None
		self.last_measured_loudness = None
		self.last_measured_loudness_time = None

	@property
	def human_id(self):
		return "%s" % self.name

	@property
	def human_frequency(self):
		return si_format(self.frequency) + "Hz"

	@property
	def human_bandwidth(self):
		return si_format(self.bandwidth) + "Hz"

	@property
	def has_parent(self):
		return self.parent is not None

	def set_present(self, signal_present, audio_present):
		if signal_present:
			if self.demodulation == DemodulationType.OFF:
				self.state = SignalState.NORMAL
			else:
				self.state = SignalState.NORMAL if audio_present else SignalState.MUTED
		else:
			self.state = SignalState.ABSENT

	def set_last_measured_audio_loudness(self, loudness):
		self.last_measured_loudness = loudness
		self.last_measured_loudness_time = time.time()

	def set_last_measured_power(self, power):
		self.last_measured_power = power
		self.last_measured_power_time = time.time()

	def to_dict(self):
		return {
			"name": self.name,
			"frequency": self.frequency,
			"bandwidth": self.bandwidth,
			"demodulation": self.demodulation.name,
			"threshold_volume": self.threshold_volume,
			"threshold_signal": self.threshold_signal,
			"parent": None if self.parent is None else self.parent.to_dict(),
		}

	@classmethod
	def from_dict(cls, data):
		parent = None
		if data["parent"] is not None:
			parent = cls.from_dict(data["parent"])

		signal = cls(
			data["name"],
			data["frequency"],
			data["bandwidth"],
			threshold_signal=data["threshold_signal"],
			demodulation=[d for d in DemodulationType if d.name == data["demodulation"]][0],
			threshold_volume=data["threshold_volume"],
			parent=parent
		)
		return signal

	def __repr__(self):
		return f"<Signal \"%s\" freq=%s bw=%s state=%s demod=%r thresh_volume=%r thresh_signal=%r%s>" % (
			self.name,
			self.frequency,
			self.bandwidth,
			self.state,
			self.demodulation,
			self.threshold_volume,
			self.threshold_signal,
			"" if self.parent is None else f" from=%r" % self.parent
		)
