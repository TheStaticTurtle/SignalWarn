from si_prefix import si_format

class Signal:
	def __init__(self, name, frequency, bandwidth, parent=None):
		self.name = name
		self.frequency = frequency
		self.bandwidth = bandwidth
		self.parent = parent

	@property
	def human_id(self):
		return "%s" % (self.name)
	@property
	def human_frequency(self):
		return si_format(self.frequency)+"Hz"
	@property
	def human_bandwidth(self):
		return si_format(self.bandwidth)+"Hz"

	def __repr__(self):
		return f"<Signal \"%s\" freq=%s bw=%s%s>" % (
			self.name,
			self.frequency,
			self.bandwidth,
			"" if self.parent is None else f" from=%r" % self.parent
		)
