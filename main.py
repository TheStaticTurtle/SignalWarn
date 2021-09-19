from pylab import *

from sdr.RtlSDR import RtlSDR

sdr = RtlSDR(debug=False)

# Tests
# print(sdr.check_frequency(95.5e6, bandwidth=12.5e3, min_power=-35, enable_de_emphasis=False))

sdr.debug = False
while True:
	print(sdr.check_frequency(95.5e6, bandwidth=50.5e3, min_power=-70, enable_de_emphasis=False))