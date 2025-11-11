import os
import platform
from pathlib import Path

class Player:
    def __init__(self):
        """Get the path to the death marker file based on OS"""
        if platform.system() == "Windows":
            base_path = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~')))
            config_dir = base_path / '.roulette'
        else:  # Linux, macOS, etc.
            config_dir = Path.home() / '.config' / 'roulette'
        
        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        self.death_file = config_dir / '.death_marker'


    def is_dead(self):
        return self.death_file.exists()


    def mark_dead(self):
        with open(self.death_file, 'w') as f:
            f.write("DEAD\n")