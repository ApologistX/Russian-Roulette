import os
import platform
from pathlib import Path
from datetime import datetime

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
    
    
    def get_death_time(self):
        """Get the timestamp when player died"""
        if not self.death_file.exists():
            return None
        
        try:
            with open(self.death_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    return lines[1].strip()
        except Exception:
            pass
        
        return None


    def mark_dead(self):
        """Mark player as dead with timestamp"""
        death_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.death_file, 'w') as f:
            f.write("DEAD\n")
            f.write(f"{death_time}\n")
    
    
    def revive(self):
        """Remove death marker - used when consuming a life"""
        if self.death_file.exists():
            self.death_file.unlink()


class HardcorePlayer:
    """Hardcore mode player - uses separate config directory"""
    def __init__(self):
        """Get the path to the death marker file based on OS"""
        if platform.system() == "Windows":
            base_path = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~')))
            config_dir = base_path / '.roulette_hardcore'
        else:  # Linux, macOS, etc.
            config_dir = Path.home() / '.config' / 'roulette_hardcore'
        
        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        self.death_file = config_dir / '.death_marker'


    def is_dead(self):
        return self.death_file.exists()
    
    
    def get_death_time(self):
        """Get the timestamp when player died"""
        if not self.death_file.exists():
            return None
        
        try:
            with open(self.death_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    return lines[1].strip()
        except Exception:
            pass
        
        return None


    def mark_dead(self):
        """Mark player as dead with timestamp"""
        death_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.death_file, 'w') as f:
            f.write("DEAD\n")
            f.write(f"{death_time}\n")
    
    
    def revive(self):
        """Remove death marker - used when consuming a life"""
        if self.death_file.exists():
            self.death_file.unlink()
