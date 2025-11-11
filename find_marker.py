from pathlib import Path
import os, platform

""" If you wish to revive yourself, you must go through the holy trial of finding the death marker file. """

if platform.system() == "Windows":
    base = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~')))
    config_dir = base / '.roulette'
else:
    config_dir = Path.home() / '.config' / 'roulette'

path = config_dir / '.death_marker'

print("LOCALAPPDATA:", os.getenv('LOCALAPPDATA'))
print("Base Path:", base)
print("Config Dir:", config_dir)
print("Death File:", path)
print("Resolved:", path.resolve())
print("Exists:", path.exists())
