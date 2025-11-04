import os
import sys

from config import BAT_NAME

def app_dir() -> str:
  if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    return sys._MEIPASS
  return os.path.dirname(os.path.abspath(__file__))

def exeutable_path() -> str:
  if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    return os.path.dirname(sys.executable)
  return os.path.dirname(os.path.abspath(__file__))

def fixed_bat_path() -> str:
  return os.path.join(exeutable_path(), BAT_NAME)
