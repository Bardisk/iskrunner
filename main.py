from runner import Runner
from utils import app_dir, fixed_bat_path

if __name__ == "__main__":
  print(f"{fixed_bat_path()}")
  print(f"{app_dir()}")
  Runner().run()