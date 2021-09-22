import threading

from sdr.BackgroundSdrThread import BackgroundSdrThread
from sdr.RtlSDR import RtlSDR
from gui.gui import Gui
from tools.DemodulationType import DemodulationType
from tools.Signal import Signal
from tools.SignalLibrary import SignalLibrary
from tools.SignalManager import SignalManager

libA = SignalLibrary()
libA.signals = {
	"CategoryA": [
		Signal("SignalA", 137.9e6, 100e3, demodulation=DemodulationType.OFF),
		Signal("SignalB", 137.1e6, 100e3),
	],
	"CategoryAA": [
		Signal("SignalA", 1145.9e6, 100e3, demodulation=DemodulationType.FM),
		Signal("SignalB", 1148.8e6, 25e3),
	],
	"CategoryB": [
		Signal("SignalC", 145.9e6, 100e3, demodulation=DemodulationType.AM),
		Signal("SignalD", 148.8e6, 25e3),
	]
}

signal_libraries = [libA]
signals_manager = SignalManager()

sdr = RtlSDR(debug=False)

sdrWorkerThread = BackgroundSdrThread(sdr, signals_manager)
sdrWorkerThread.start()

gui = Gui(signal_libraries, signals_manager)
gui.run()

sdrWorkerThread.quit()
sdrWorkerThread.join()

# sdr = RtlSDR(debug=False)
#
# # Tests
# # print(sdr.check_frequency(95.5e6, bandwidth=12.5e3, min_power=-35, enable_de_emphasis=False))
#
# sdr.debug = False
# while True:
# 	print(sdr.check_frequency(95.5e6, bandwidth=50.5e3, min_power=-70, enable_de_emphasis=False))