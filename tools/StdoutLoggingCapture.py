import logging
import os
import platform
import threading
import time

if platform.system() == "Windows":
	import msvcrt
	from ctypes import windll, byref, wintypes, GetLastError, WinError, POINTER
	from ctypes.wintypes import HANDLE, DWORD, BOOL

	LPDWORD = POINTER(DWORD)
	PIPE_NOWAIT = wintypes.DWORD(0x00000001)
	ERROR_NO_DATA = 232
else:
	import fcntl
	import select


class StdoutLoggingCapture:
	def __init__(self, logger_name):
		self.logger = logging.getLogger(logger_name)

	def __enter__(self):
		self.text_stdout = b""
		self.text_stderr = b""
		self._pipe_out, self._pipe_in = os.pipe()
		self._err_pipe_out, self._err_pipe_in = os.pipe()
		self.set_nonblocking(self._pipe_out)
		self.set_nonblocking(self._err_pipe_out)

		self._stdout = os.dup(1)
		self._stderr = os.dup(2)

		os.dup2(self._pipe_in, 1)
		os.dup2(self._err_pipe_in, 2)

		self._stop = False
		self._read_thread = threading.Thread(target=self._bg_read_stdout, args=[self._pipe_out])
		self._read_err_thread = threading.Thread(target=self._bg_read_stderr, args=[self._err_pipe_out])
		self._read_thread.start()
		self._read_err_thread.start()

		return self

	def __exit__(self, *args):
		self._stop = True
		self._read_thread.join()
		self._read_err_thread.join()

		os.dup2(self._stdout, 1)
		os.dup2(self._stderr, 2)

		self.text_stdout += self.read_pipe(self._pipe_out)
		self.text_stderr += self.read_pipe(self._err_pipe_out)
		if self.text_stdout:
			self.logger.info(self.text_stdout.decode("utf-8").replace("\n","").replace("\r",""))
		if self.text_stderr:
			self.logger.warning(self.text_stderr.decode("utf-8").replace("\n","").replace("\r",""))

	def set_nonblocking(self, file_handle):
		"""
		Makes the file descriptor non blocking.
		"""
		if platform.system() == "Windows":
			# See https://stackoverflow.com/a/34504971/11106801
			SetNamedPipeHandleState = windll.kernel32.SetNamedPipeHandleState
			SetNamedPipeHandleState.argtypes = [HANDLE, LPDWORD, LPDWORD, LPDWORD]
			SetNamedPipeHandleState.restype = BOOL

			handle = msvcrt.get_osfhandle(file_handle)

			res = windll.kernel32.SetNamedPipeHandleState(handle, byref(PIPE_NOWAIT), None, None)
		else:
			OFLAGS = fcntl.fcntl(file_handle, fcntl.F_GETFL)
			nflags = OFLAGS | os.O_NONBLOCK
			fcntl.fcntl(file_handle, fcntl.F_SETFL, nflags)


		return not (res == 0)
	def has_more_data(self, pipe):
		if platform.system() == "Windows":
			return True
		r, _, _ = select.select([pipe], [], [], 0)
		return bool(r)

	def read_pipe(self, pipe):
		out = b''
		try:
			while self.has_more_data(pipe):
				out += os.read(pipe, 1024)
		except OSError as error:
			err_code = GetLastError()
			if err_code == ERROR_NO_DATA:
				pass
			else:
				raise error

		return out

	def _bg_read_stdout(self, pipe):
		while not self._stop:
			self.text_stdout += self.read_pipe(pipe)
			if b"\n" in self.text_stdout:
				self.log(self.text_stdout.split(b"\n")[0])
				self.text_stdout = self.text_stdout.split(b"\n")[1]
			time.sleep(0.001)
	def _bg_read_stderr(self, pipe):
		while not self._stop:
			self.text_stderr += self.read_pipe(pipe)
			if b"\n" in self.text_stderr:
				self.log_err(self.text_stderr.split(b"\n")[0])
				self.text_stderr = self.text_stderr.split(b"\n")[1]
			time.sleep(0.001)

	def log(self,text:bytes):
		if text:
			os.dup2(self._stdout, 1)
			self.logger.info(text.decode("utf-8"))
			os.dup2(self._pipe_in, 1)
	def log_err(self,text:bytes):
		if text:
			os.dup2(self._stdout, 1)
			self.logger.warning(text.decode("utf-8"))
			os.dup2(self._pipe_in, 1)

