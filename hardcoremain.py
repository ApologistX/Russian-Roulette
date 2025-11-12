#!/usr/bin/env python3
"""
Hardcore Russian Roulette - A simulated game of chance
The game tracks deaths permanently via a hidden config file.
Lives system allows extra chances at the risk of destroying your system.
⚠️The lives system will choose a random file from System32 on windows, or root⚠️
- All deleted system files will be stored in a logs folder.
There's a prompt before you delete the file. Type Sacrafice to keep dancing with death.
"""

import os
import platform
import random
import time
from datetime import datetime
from pathlib import Path
from art_utils import Art
from player_utils import Player, HardcorePlayer

player = Player()
hardcore_player = HardcorePlayer()


class LivesManager:
    def __init__(self, lives_folder="./lives"):
        self.lives_folder = Path(lives_folder)
        self.debug_mode = False  # Debug mode toggle
        
        # Get config directory based on OS (same location as death marker)
        if platform.system() == "Windows":
            base_path = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~')))
            self.config_dir = base_path / '.roulette'
        else:  # Linux, macOS, etc.
            self.config_dir = Path.home() / '.config' / 'roulette'
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Path to death marker file
        self.death_marker = self.config_dir / '.death_marker'
        
        # Create lives folder if it doesn't exist
        self.lives_folder.mkdir(exist_ok=True)
        
        # Generate initial life file if folder is empty
        self._generate_initial_life()
    
    def _generate_initial_life(self):
        """Create one initial life file"""
        # Check if any files exist in the folder first
        existing_files = list(self.lives_folder.iterdir()) if self.lives_folder.exists() else []
        
        # Check if a "first run" marker exists in config directory
        first_run_marker = self.config_dir / ".first_run_complete"
        
        # Only create starter life if:
        # 1. Folder is empty (no files)
        # 2. AND first run marker doesn't exist (never played before)
        if len(existing_files) == 0 and not first_run_marker.exists():
            initial_life = self.lives_folder / "starter_life.txt"
            
            # Create the file
            initial_life.write_text("Your first life. Good luck.")
            
            # Create first run marker so we don't generate lives again
            first_run_marker.touch()
            
            print(f"💚 Starter life created: {initial_life.name}")
    
    def _get_cutoff_date(self):
        """Get the cutoff date for valid lives (death time or current time)"""
        if self.death_marker.exists():
            # Use death marker file's creation time as cutoff
            return self.death_marker.stat().st_mtime
        else:
            # If not dead, use current time (all existing files are valid)
            return time.time()
    
    def get_valid_lives(self, show_debug=None):
        """Get list of valid life files (modified before cutoff date)"""
        if not self.lives_folder.exists():
            return []
        
        # Get cutoff date dynamically
        cutoff_date = self._get_cutoff_date()
        
        # If show_debug is explicitly False, don't show debug
        # If show_debug is None, use self.debug_mode
        # If show_debug is True, always show debug
        if show_debug is False:
            should_debug = False
        elif show_debug is True:
            should_debug = True
        else:
            should_debug = self.debug_mode
        
        valid_lives = []
        for file_path in self.lives_folder.iterdir():
            if file_path.is_file():
                mod_time = file_path.stat().st_mtime  # Use modification time instead of creation time
                
                # Only show debug output if debug mode is enabled
                if should_debug:
                    print(f"DEBUG: Checking {file_path.name}")
                    print(f"  Modified time: {mod_time}")
                    print(f"  Cutoff time: {cutoff_date}")
                    print(f"  Valid: {mod_time < cutoff_date}")
                
                if mod_time < cutoff_date:
                    valid_lives.append(file_path)
        
        return sorted(valid_lives, key=lambda x: x.stat().st_mtime)
    
    def count_lives(self):
        """Count number of valid lives remaining"""
        return len(self.get_valid_lives())
    
    def consume_life(self):
        """Use up one life (delete oldest valid life file)"""
        valid_lives = self.get_valid_lives()
        
        if not valid_lives:
            return False
        
        # Delete the oldest life file
        oldest_life = valid_lives[0]
        try:
            oldest_life.unlink()
            print(f"\n💚 EXTRA LIFE CONSUMED!")
            print(f"   Used: {oldest_life.name}")
            print(f"   Lives remaining: {self.count_lives()}")
            return True
        except Exception as e:
            print(f"Error consuming life: {e}")
            return False
    
    def has_lives(self):
        """Check if player has any lives remaining"""
        return self.count_lives() > 0


class HardcoreLivesManager:
    """Hardcore version - sacrifices real system files"""
    def __init__(self):
        self.debug_mode = False
        
        # Determine system file directory based on OS
        if platform.system() == "Windows":
            self.sacrifice_dir = Path("C:/Windows/System32")
        else:  # Linux, macOS
            self.sacrifice_dir = Path("/")
        
        # Get config directory for death marker
        if platform.system() == "Windows":
            base_path = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~')))
            self.config_dir = base_path / '.roulette_hardcore'
        else:
            self.config_dir = Path.home() / '.config' / 'roulette_hardcore'
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.death_marker = self.config_dir / '.death_marker'
        
        # Log file for deleted files
        self.sacrifice_log = self.config_dir / 'sacrifices.log'
    
    def _get_random_system_file(self):
        """Get a random file from the system directory (not a folder)"""
        try:
            all_files = []
            
            # For Windows System32
            if platform.system() == "Windows":
                # Only scan System32 directory (not subdirectories)
                for item in self.sacrifice_dir.iterdir():
                    if item.is_file():
                        all_files.append(item)
            else:
                # For Linux/Unix, only scan root directory files
                for item in self.sacrifice_dir.iterdir():
                    if item.is_file():
                        all_files.append(item)
            
            if not all_files:
                return None
            
            return random.choice(all_files)
        
        except PermissionError:
            print("Permission denied accessing system files.")
            return None
        except Exception as e:
            print(f"Error accessing system files: {e}")
            return None
    
    def has_lives(self):
        """In hardcore mode, you always have 'lives' if system files exist"""
        # Try to find at least one accessible file
        return self._get_random_system_file() is not None
    
    def consume_life(self):
        """Delete a random system file as sacrifice"""
        victim_file = self._get_random_system_file()
        
        if not victim_file:
            print("\nNo accessible system files found to sacrifice!")
            return False
        
        print(f"\nHARDCORE MODE: SYSTEM FILE SACRIFICE REQUIRED")
        print(f"Selected victim: {victim_file}")
        print(f"Location: {victim_file.parent}")
        print(f"\nTHIS WILL DELETE A REAL SYSTEM FILE!")
        print(f"THIS MAY BREAK YOUR SYSTEM!")
        
        confirmation = input("\nType 'SACRIFICE' to delete this file and revive: ").strip()
        
        if confirmation != "SACRIFICE":
            print("\nSacrifice refused. You remain dead.")
            return False
        
        try:
            # Log the sacrifice before deletion
            with open(self.sacrifice_log, 'a') as log:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"{timestamp} | DELETED: {victim_file}\n")
            
            # Attempt to delete the file
            victim_file.unlink()
            
            print(f"\nSYSTEM FILE DELETED!")
            print(f"   Sacrificed: {victim_file.name}")
            print(f"   Logged to: {self.sacrifice_log}")
            print(f"\nYour system may now be unstable.")
            
            return True
        
        except PermissionError:
            print(f"\nPermission denied. Cannot delete {victim_file.name}")
            print("   (This shouldn't happen with elevated permissions)")
            print("   You remain dead.")
            return False
        except Exception as e:
            print(f"\nError deleting file: {e}")
            print("   You remain dead.")
            return False
    
    def count_lives(self):
        """In hardcore mode, lives are theoretical (system files available)"""
        return "???" if self.has_lives() else 0


# Global instances
lives_manager = LivesManager()
hardcore_lives = HardcoreLivesManager()


def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def spin_cylinder():
    """Simulate spinning the revolver's cylinder with ASCII art"""
    artwork = Art("./Art/")
    frames = [artwork.Alive, artwork.Dead]

    clear_screen()
    print("\n You spin the cylinder...\n")
    time.sleep(1)
    
    # Spin animation
    for _ in range(len(frames) * 3):
        for frame in frames:
            print(frame)
            time.sleep(0.08)
            clear_screen()
    
    # Final position
    print(frames[0])
    time.sleep(0.3)


def play_round():
    """Play one round of Russian Roulette with lives system"""
    chamber = random.randint(1, 6)
    
    print("\n Russian Roulette")
    print("=" * 40)
    # Force no debug output when just displaying lives count
    lives_count = len(lives_manager.get_valid_lives(show_debug=False))
    if lives_count > 0:
        print(f"💚 Extra Lives: {lives_count}")
    input("Press ENTER to spin the cylinder...")
    
    spin_cylinder()
    
    print("\n" + "=" * 40)
    input("Press ENTER to pull the trigger...")
    
    print("\n*CLICK*\n")
    time.sleep(0.5)
    
    if chamber == 1:  # 1 in 6 chance
        # 33% chance of failure (jam or dud)
        if random.random() < 0.33:
            # 50-50 chance: gun jam or dud ammo
            if random.random() < 0.5:
                print("🔧 *CLUNK* - THE GUN JAMMED!")
                print("Mechanical failure! The firing pin didn't strike!")
            else:
                print("💨 *THUNK* - DUD ROUND!")
                print("The primer failed to ignite! Faulty ammunition!")
            print("\nYou survive by sheer luck!")
            print("The cylinder rotates. The game continues...\n")
            time.sleep(1.5)
            return True  # Survived
        else:
            print("💀 BANG! You're dead!")
            
            # Check for extra lives
            if lives_manager.has_lives():
                time.sleep(1)
                if lives_manager.consume_life():
                    print("\n🔄 You've been revived!")
                    print("The game continues...\n")
                    time.sleep(1.5)
                    return True  # Continue playing
            
            # No lives left - permanent death
            print("\nGame Over. You can NEVER play again.")
            player.mark_dead()
            return False
    else:
        print("✓ You survived this round!")
        print(f"Chamber {chamber}/6 was empty.")
        return True


def play_round_hardcore():
    """Play one round with hardcore revival system"""
    chamber = random.randint(1, 6)
    print("By playing you assume all liability for damages.")
    print("\n 🔥Russian Roulette - HARDCORE MODE🔥")
    print("=" * 40)
    print("System File Sacrifice: Available" if hardcore_lives.has_lives() else "No system files available")
    input("Press ENTER to spin the cylinder...")
    
    spin_cylinder()
    
    print("\n" + "=" * 40)
    input("Press ENTER to pull the trigger...")
    
    print("\n*CLICK*\n")
    time.sleep(0.5)
    
    if chamber == 1:  # 1 in 6 chance
        # 13% chance of failure (jam or dud)
        if random.random() < 0.13:
            # 50-50 chance: gun jam or dud ammo
            if random.random() < 0.5:
                print("*CLUNK* - THE GUN JAMMED!")
                print("Mechanical failure! The firing pin didn't strike!")
            else:
                print("*THUNK* - DUD ROUND!")
                print("The primer failed to ignite! Faulty ammunition!")
            print("\nYou survive by sheer luck!")
            print("The cylinder rotates. The game continues...\n")
            time.sleep(1.5)
            return True  # Survived
        else:
            print("BANG! You're dead!")
            
            # Check for hardcore revival
            if hardcore_lives.has_lives():
                time.sleep(1)
                if hardcore_lives.consume_life():
                    hardcore_player.revive()
                    print("\nYou've been revived through sacrifice!")
                    print("The game continues...\n")
                    time.sleep(1.5)
                    return True  # Continue playing
            
            # No lives left - permanent death
            print("\nGame Over. You can NEVER play again.")
            hardcore_player.mark_dead()
            return False
    else:
        print("You survived this round!")
        print(f"Chamber {chamber}/6 was empty.")
        return True


if __name__ == "__main__":
    import sys

    from player_utils import HardcorePlayer
    hardcore_player = HardcorePlayer()

    if hardcore_player.is_dead():
        print("💀 You are permanently dead.")
        death_time = hardcore_player.get_death_time()
        if death_time:
            print(f"You died on {death_time}. You can never play again.")
        sys.exit(0)

    print("🔥 Welcome to Russian Roulette (Hardcore Mode) 🔥")
    print("You only live once. Survive as long as you can.\n")


    alive = True
    while alive:
        alive = play_round_hardcore()
        
        if not alive:
            print("\n💀 Your journey ends here.")
            break 
            
        print("\n" + "=" * 40) 
        again = input("\nPlay another round? (y/n): ").strip().lower()
        
        if again != 'y': 
            print("\nYou walk away alive. Wise choice.")
            break 
