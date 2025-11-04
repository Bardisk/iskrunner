from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from config import TITLE

class LogWindow(QMainWindow):
  def __init__(self, icon: QIcon | None = None):
    super().__init__()

    if icon is not None:
      self.setWindowIcon(icon)

    self.setWindowTitle(f"{TITLE} - log")
    self.resize(820, 520)
    self.text = QPlainTextEdit()
    self.text.setReadOnly(True)
    self.text.setLineWrapMode(QPlainTextEdit.NoWrap)
    central = QWidget()
    lay = QVBoxLayout(central)
    lay.addWidget(self.text)
    self.setCentralWidget(central)

  def append(self, s: str):
    self.text.appendPlainText(s)
    self.text.verticalScrollBar().setValue(self.text.verticalScrollBar().maximum())

  def clear(self):
    self.text.clear()
