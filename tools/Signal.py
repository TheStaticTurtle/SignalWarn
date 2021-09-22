from enum import Enum
from si_prefix import si_format

class SignalState(Enum):
	UNKNOWN = 0,
	NORMAL = 1,
	MUTED = 2,
	ABSENT = 3,

class Signal:
	def __init__(self, name, frequency, bandwidth, parent=None):
		self.name = name
		self.frequency = frequency
		self.bandwidth = bandwidth
		self.parent = parent
		self.state = SignalState.UNKNOWN

	@property
	def human_id(self):
		return "%s" % (self.name)
	@property
	def human_frequency(self):
		return si_format(self.frequency)+"Hz"
	@property
	def human_bandwidth(self):
		return si_format(self.bandwidth)+"Hz"
	@property
	def has_parent(self):
		return self.parent is not None

	def __repr__(self):
		return f"<Signal \"%s\" freq=%s bw=%s state=%s%s>" % (
			self.name,
			self.frequency,
			self.bandwidth,
			self.state,
			"" if self.parent is None else f" from=%r" % self.parent
		)
