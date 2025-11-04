import subprocess
import threading
import signal
import os
import time

from PyQt5.QtCore import QObject, pyqtSignal

from utils import app_dir

class ProcController(QObject):
  line_signal = pyqtSignal(str)
  status_signal = pyqtSignal(str)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.proc: subprocess.Popen | None = None
    self.reader_thread: threading.Thread | None = None
    self._stop_reader = threading.Event()

  def is_running(self) -> bool:
    return self.proc is not None and (self.proc.poll() is None)

  def start(self, bat_path: str):
    if self.is_running():
      self.status_signal.emit("Process is already running.")
      return

    if not os.path.exists(bat_path):
      self.status_signal.emit(f"Script not found: {bat_path}")
      return

    CREATE_NO_WINDOW = 0x08000000

    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = 0  # SW_HIDE

    cmd = ['cmd.exe', '/Q', '/C', bat_path]

    try:
      self.proc = subprocess.Popen(
        cmd,
        cwd=app_dir(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
        creationflags=CREATE_NO_WINDOW,
        startupinfo=si
      )
      self.status_signal.emit(f"Started: {bat_path}")
    except Exception as e:
      self.proc = None
      self.status_signal.emit(f"Failed to start: {e}")
      return

    # Launch output reader thread
    self._stop_reader.clear()
    self.reader_thread = threading.Thread(target=self._read_output_loop, daemon=True)
    self.reader_thread.start()

  def _read_output_loop(self):
    if not self.proc or not self.proc.stdout:
      return
    for line in self.proc.stdout:
      if self._stop_reader.is_set():
        break
      self.line_signal.emit(line.rstrip('\r\n'))

    if self.proc:
      rc = self.proc.wait()
      self.status_signal.emit(f"Process exited with code: {rc}")

  def send_ctrl_break(self):
    if self.is_running():
      try:
        os.kill(self.proc.pid, signal.CTRL_BREAK_EVENT)  # Send to process group
        self.status_signal.emit("CTRL_BREAK sent.")
      except Exception as e:
        self.status_signal.emit(f"Failed to send CTRL_BREAK: {e}")

  def terminate_tree(self, timeout=3.0):
    if not self.is_running():
      return

    self.send_ctrl_break()
    start = time.time()
    while self.is_running() and (time.time() - start) < timeout:
      time.sleep(0.01)

    if self.is_running():
      try:
        subprocess.run(
          ["taskkill", "/PID", str(self.proc.pid), "/T", "/F"],
          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        self.status_signal.emit("taskkill /T /F executed.")
      except Exception as e:
        self.status_signal.emit(f"taskkill failed: {e}")

    self._stop_reader.set()
    try:
      if self.reader_thread and self.reader_thread.is_alive():
        self.reader_thread.join(timeout=1.0)
    except Exception:
      pass

    self.proc = None
    self.reader_thread = None

