#!/usr/bin/env python3
"""
Library for holding game functionality.
"""

import os
import platform
import random
import time
from art_utils import Art
from player_utils import Player

player = Player()

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
    """Play one round of Russian Roulette"""
    chamber = random.randint(1, 6)
    
    print("\n Russian Roulette")
    print("=" * 40)
    input("Press ENTER to spin the cylinder...")
    
    spin_cylinder()
    
    print("\n" + "=" * 40)
    input("Press ENTER to pull the trigger...")
    
    print("\n*CLICK*\n")
    time.sleep(0.5)
    
    if chamber == 1:  # 1 in 6 chance
        print("💀 BANG! You're dead!")
        print("\nGame Over. You can NEVER play again.")
        player.mark_dead()
        return False
    else:
        print("✓ You survived this round!")
        print(f"Chamber {chamber}/6 was empty.")
        return True