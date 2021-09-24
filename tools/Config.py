import json
import logging
import os
import os.path
import pathlib
import sys

from tools.SignalManager import SignalManager

default_config = {
	"ui": {
		"color": {
			"signal_absent": (255, 0, 0),
			"signal_absent_faded": (100, 0, 0),
			"signal_muted": (252, 186, 3),
			"signal_muted_faded": (156, 115, 3),
			"signal_normal": (87, 181, 54),
			"signal_normal_faded": (87, 181, 54),
			"signal_unknown": (70, 70, 70),
			"signal_unknown_faded": (100, 100, 100),
			"checking_signal": (0, 217, 255),
			"checking_signal_faded": (0, 167, 196),
		},
	},
	"radio": {
		"sdr": {
			"samples_per_measurement": 512 * 1024,
			"capture_offset": 250e3,
			"sample_rate": 2.4e6,
			"settle_time": 0.01
		},
		"processing": {
			"minimum_filter_bw": 100e3,
			"enable_de_emphasis": False
		}
	}
}


def get_user_data_dir(appname):
	if sys.platform == "win32":
		import winreg
		key = winreg.OpenKey(
			winreg.HKEY_CURRENT_USER,
			r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
		)
		dir_, _ = winreg.QueryValueEx(key, "Local AppData")
		out = pathlib.Path(dir_).resolve(strict=False)
	elif sys.platform == 'darwin':
		out = pathlib.Path('~/Library/Application Support/').expanduser()
	else:
		out = pathlib.Path(os.getenv('XDG_DATA_HOME', "~/.local/share")).expanduser()
	return out.joinpath(appname)


class Config:
	def __init__(self, signals_manager: SignalManager):
		self.signals_manager = signals_manager
		self.logger = logging.getLogger(self.__class__.__name__)
		self.home_path = get_user_data_dir("SignalWarn")
		self.config_file_path = os.path.join(self.home_path, "config.json")
		self.snapshot_file_path = os.path.join(self.home_path, "last_signals.json")
		self._config = {}

		self.logger.debug("Hellow, checking home folder")
		if not os.path.exists(self.home_path):
			os.makedirs(self.home_path)
			self.logger.info("Created directory %s" % self.home_path)

		self.init_config()
		self.init_last_signals()

	def init_config(self):
		if not os.path.exists(self.config_file_path):
			self.logger.info("Saving default config to: %s" % self.config_file_path)
			self._config = self.correct_dict(self._config, default_config)
		else:
			self.logger.info("Loading config saved at: %s" % self.config_file_path)
			self.load_config()

		self.save_config()

	def init_last_signals(self):
		if not os.path.exists(self.snapshot_file_path):
			self.logger.info("No signals detected form last session, saving empty file")
		else:
			self.logger.info("Loading previous session signals from: %s " % self.snapshot_file_path)
			self.signals_manager.load(self.snapshot_file_path)

		self.signals_manager.save(self.snapshot_file_path)

	def correct_dict(self, data, against, parent_key=""):
		out = {}
		for key in data.keys():
			if key not in against.keys():
				self.logger.warning("Unknown key %s%s found in config" % (parent_key, key))
			else:
				if isinstance(data[key], dict):
					out[key] = self.correct_dict(data[key], against[key], parent_key=parent_key + key + ".")
				else:
					# TODO: Maybe check type IDK
					out[key] = data[key]
					pass

		for key in against.keys():
			if key not in data.keys():
				self.logger.warning("Missing key found in config: %s%s" % (parent_key, key))
				if isinstance(against[key], dict):
					out[key] = self.correct_dict(data[key], against[key], parent_key=parent_key + key + ".")
				else:
					out[key] = against[key]

		return out

	def load_config(self, path=None):
		if path is None:
			path = self.config_file_path
		self.logger.info("Loading config from %s" % path)
		saved_conf = json.loads(open(path).read())
		self._config = self.correct_dict(saved_conf, default_config)

	def save_config(self, path=None):
		if path is None:
			path = self.config_file_path
		self.logger.info("Saving config to %s" % path)
		data = json.dumps(self._config, indent=4)
		open(path, "w").write(data)

	def get(self, property_chain, default):
		chains = property_chain.split(".")

		chain = None
		try:
			value = self._config
			for chain in chains:
				value = value[chain]
			return value
		except KeyError as e:
			self.logger.error("Coulnd't find key \"%s\" stuck at chain \"%s\", returning default value" % (property_chain, chain))
			return default

	def on_exit(self):
		self.signals_manager.save(self.snapshot_file_path)

	def set(self, property_chain, value):
		chains = property_chain.split(".")

		def chain_to_dict(c):
			return "self._config" + "".join(["[\""+x+"\"]" for x in c])
		
		for i in range(len(chains)-1):
			tmp = chains[:i+1]
			try:
				eval(chain_to_dict(tmp))
			except KeyError:
				self.logger.warning("Setting unknown key %s" % '.'.join(tmp))
				exec(chain_to_dict(tmp) + " = {}")
		exec(chain_to_dict(chains) + " = value")

		self.save_config()

