import os
import sys

from controller import ProcController
from logw import LogWindow

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCursor

from config import TITLE, ICON_PATH
from utils import app_dir, fixed_bat_path

class Runner:
  def __init__(self):
    self.app = QApplication(sys.argv)
    self.app.setQuitOnLastWindowClosed(False)

    icon = QIcon(os.path.join(app_dir(), ICON_PATH)) if os.path.exists(os.path.join(app_dir(), ICON_PATH)) else QIcon()
    self.tray = QSystemTrayIcon(icon)
    self.tray.setToolTip(TITLE)

    self.menu = QMenu()
    self.act_show = QAction("Log")
    self.act_restart = QAction("Restart")
    self.act_exit = QAction("Exit")
    self.act_show.triggered.connect(self.toggle_log)
    self.act_restart.triggered.connect(self.restart_proc)
    self.act_exit.triggered.connect(self.exit_app)
    self.menu.addAction(self.act_show)
    self.menu.addAction(self.act_restart)
    self.menu.addSeparator()
    self.menu.addAction(self.act_exit)

    self.tray.setContextMenu(self.menu)
    self.tray.show()

    self.tray.activated.connect(self.on_tray_activated)

    self.log_win = LogWindow(icon)

    self.proc = ProcController()
    self.proc.line_signal.connect(self.log_win.append)
    self.proc.status_signal.connect(self.on_status)

    QTimer.singleShot(0, self.start_fixed_bat)

  def on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason):
    if reason == QSystemTrayIcon.Trigger:
      self.toggle_log()

  def toggle_log(self):
    if self.log_win.isVisible():
      self.log_win.hide()
    else:
      self.log_win.show()
      self.log_win.activateWindow()
      self.log_win.raise_()

  def start_fixed_bat(self):
    self.log_win.append(f"[INFO] Launched: {fixed_bat_path()}")
    self.proc.start(fixed_bat_path())

  def restart_proc(self):
    self.log_win.append("[INFO] Terminating process...")
    self.proc.terminate_tree(timeout=2.0)
    self.log_win.append(f"[INFO] Restarting: {fixed_bat_path()}")
    self.proc.start(fixed_bat_path())

  def on_status(self, msg: str):
    self.log_win.append(f"[STATUS] {msg}")

  def exit_app(self):
    self.log_win.append("[INFO] Exiting application, terminating subprocess...")
    self.proc.terminate_tree(timeout=0.1)
    QSystemTrayIcon.hide(self.tray)
    QApplication.quit()

  def run(self):
    sys.exit(self.app.exec_())

