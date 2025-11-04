from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

from config import TITLE

class LogWindow(QMainWindow):
  send_clicked = pyqtSignal(str)

  def __init__(self, icon: QIcon | None = None):
    super().__init__()

    if icon is not None:
      self.setWindowIcon(icon)

    self.setWindowTitle(f"{TITLE} - Console")
    self.resize(820, 560)

    self.input_edit = QLineEdit()
    self.input_edit.setPlaceholderText("Type a command here")
    self.btn_send = QPushButton("Send")
    self.btn_send.setDefault(True)
    self.btn_send.clicked.connect(self._on_send)
    self.input_edit.returnPressed.connect(self._on_send)

    bottom = QWidget()
    h = QHBoxLayout(bottom)
    h.setContentsMargins(0, 0, 0, 0)
    h.addWidget(self.input_edit)
    h.addWidget(self.btn_send)

    self.text = QPlainTextEdit()
    self.text.setReadOnly(True)
    self.text.setLineWrapMode(QPlainTextEdit.NoWrap)
    central = QWidget()
    lay = QVBoxLayout(central)
    lay.addWidget(self.text)
    lay.addWidget(bottom)
    self.setCentralWidget(central)

  def _on_send(self):
    s = self.input_edit.text()
    if not s:
        return
    self.send_clicked.emit(s)
    self.append(f">>> {s}")
    self.input_edit.clear()

  def set_input_enabled(self, ok: bool):
    self.input_edit.setEnabled(ok)
    self.btn_send.setEnabled(ok)

  def append(self, s: str):
    self.text.appendPlainText(s)
    self.text.verticalScrollBar().setValue(self.text.verticalScrollBar().maximum())

  def clear(self):
    self.text.clear()
