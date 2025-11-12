#!/usr/bin/env python3
"""
Russian Roulette - A simulated game of chance
The game tracks "deaths" permanently via a hidden config file.
"""

import os
import random
import sys
from game_lib import play_round, player

def main():
    """Main game loop"""
    # Check if player is already dead
    if player.is_dead():
        print("💀 You're already DEAD!")
        print("You cannot play Russian Roulette anymore.")
        print("\nThis is permanent. There is no reset.")
        sys.exit(1)
    
    print("=" * 40)
    print("   RUSSIAN ROULETTE")
    print("=" * 40)
    print("\nWelcome! The revolver has 6 chambers.")
    print("One bullet. Press ENTER to play.")
    print("⚠️  WARNING: If you die, you can NEVER play again.")
    print("This is PERMANENT. No resets.\n")
    
    try:
        while True:
            survived = play_round()
            if not survived:
                break
            
            print("\n" + "=" * 40)
            choice = input("\nPlay again? (y/n): ").strip().lower()
            if choice != 'y':
                print("\nYou walk away alive. Wise choice.")
                break
    except KeyboardInterrupt:
        print("\n\nGame interrupted. You survive... for now.")


if __name__ == "__main__":
    main()
