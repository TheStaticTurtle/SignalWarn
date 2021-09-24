import logging, sys, coloredlogs

from tools.Config import Config

coloredlogs.install(stream=sys.stdout, fmt="[%(asctime)s] [%(name)30s] [%(levelname)8s] %(message)s", level=logging.INFO)
logging.info("Hellow, world")

from sdr.BackgroundSdrThread import BackgroundSdrThread, BackgroundCheckProcessThread
from sdr.RtlSDR import RtlSDR
from gui.gui import Gui
# from tools.DemodulationType import DemodulationType
# from tools.Signal import Signal
# from tools.SignalLibrary import SignalLibrary
from signal_libraries import signal_libraries
from tools.SignalManager import SignalManager

logging.getLogger(RtlSDR.__name__).setLevel(logging.WARNING)
logging.getLogger(BackgroundCheckProcessThread.__name__).setLevel(logging.WARNING)


signals_manager = SignalManager()

config = Config(signals_manager)

sdr = RtlSDR(config, debug=False)

sdrWorkerThread = BackgroundSdrThread(config, sdr, signals_manager)
sdrWorkerThread.start()

gui = Gui(config, signal_libraries, signals_manager)
gui.run()

sdrWorkerThread.quit()
sdrWorkerThread.join()

config.on_exit()

# from tools.DemodulationType import DemodulationType
#
# sdr = RtlSDR(debug=False)
# #
# # # Tests
# print(sdr.check_frequency(103e6, bandwidth=200e3, min_power=-70, enable_de_emphasis=False, demodulate=DemodulationType.FM))
# #
# sdr.debug = False
# while True:
# 	print(sdr.check_frequency(103e6, bandwidth=200e3, min_power=-70, enable_de_emphasis=False, demodulate=DemodulationType.FM))