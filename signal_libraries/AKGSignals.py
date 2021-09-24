from tools.DemodulationType import DemodulationType
from tools.Signal import Signal
from tools.SignalLibrary import SignalLibrary

class AKGSignals(SignalLibrary):
	"""
		Frequencies used by AKG
		Reference (WMS420): https://www.soundservices.co.uk/wp-content/uploads/2017/09/UHF-wireless-mic-frequencies-AKG.pdf
	"""
	NAME = "AKG"

	def __init__(self):
		super().__init__()
		self.signals = {
			"WMS420": [
				Signal("Bank A / Channel 1", 530.025e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank A / Channel 2", 532.700e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank A / Channel 3", 540.000e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank A / Channel 4", 541.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank A / Channel 5", 546.775e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank A / Channel 6", 557.500e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank A / Channel 7", 557.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank A / Channel 8", 559.000e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U1 / Channel 1", 606.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U1 / Channel 2", 606.600e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U1 / Channel 3", 608.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U1 / Channel 4", 610.700e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U1 / Channel 5", 611.450e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U1 / Channel 6", 612.450e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U1 / Channel 7", 613.700e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U2 / Channel 1", 614.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U2 / Channel 2", 614.500e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U2 / Channel 3", 616.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U2 / Channel 4", 618.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U2 / Channel 5", 620.500e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U2 / Channel 6", 625.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U2 / Channel 7", 629.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank U2 / Channel 8", 629.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B1 / Channel 1", 748.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B1 / Channel 2", 748.500e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B1 / Channel 3", 749.500e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B1 / Channel 4", 751.200e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B1 / Channel 5", 751.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B2 / Channel 1", 774.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B2 / Channel 2", 774.500e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B2 / Channel 3", 775.500e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B2 / Channel 4", 777.200e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank B2 / Channel 5", 774.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank M / Channel 1", 826.300e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank M / Channel 2", 826.700e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank M / Channel 3", 828.450e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank M / Channel 4", 829.050e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank M / Channel 5", 829.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank M / Channel 6", 831.000e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank D / Channel 1", 863.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank D / Channel 2", 863.500e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank D / Channel 3", 864.950e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank D / Channel A", 863.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank D / Channel B", 863.675e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank D / Channel C", 864.525e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank D / Channel D", 864.900e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank K / Channel 1", 925.100e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank K / Channel 2", 925.700e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank K / Channel 3", 928.175e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank K / Channel 4", 929.075e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank K / Channel 5", 930.300e6, 200e3, demodulation=DemodulationType.FM),
				Signal("Bank K / Channel 6", 931.850e6, 200e3, demodulation=DemodulationType.FM),
			]
		}
