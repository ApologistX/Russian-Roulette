#!/usr/bin/env python3
"""
Russian Roulette - A simulated game of chance
The game tracks "deaths" permanently via a hidden config file.
Lives system allows extra chances.
"""

import os
import random
import sys
from game_lib import play_round, player, lives_manager

def main():
    """Main game loop"""
    # Check if player is dead AND has no lives
    if player.is_dead() and not lives_manager.has_lives():
        print("💀 You're already DEAD!")
        
        # Display time of death if available
        death_time = player.get_death_time()
        if death_time:
            print(f"Time of death: {death_time}")
        
        print("You cannot play Russian Roulette anymore.")
        print("\nThis is permanent. There is no reset.")
        print("Unless you sacrafice a file to the Lives directory predating your death.")
        sys.exit(1)
    
    # If dead but has lives, revive them
    if player.is_dead() and lives_manager.has_lives():
        death_time = player.get_death_time()
        print("💀 You were dead, but you have extra lives!")
        if death_time:
            print(f"   (Died at: {death_time})")
        lives_manager.consume_life()
        # Revive/Clear the death marker
        player.revive()
        print("🔄 You've been revived!\n")
    
    print("=" * 40)
    print("   RUSSIAN ROULETTE")
    print("=" * 40)
    print("\nWelcome! The revolver has 6 chambers.")
    print("One bullet. Press ENTER to play.")
    print("⚠️  WARNING: If you die, you can NEVER play again.")
    print("💚 Extra lives can save you from permanent death!")
    print("This is PERMANENT. No resets.\n")
    
    try:
        while True:
            survived = play_round()
            if not survived:
                break
            
            print("\n" + "=" * 40)
            choice = input("\nPlay again? (y/n): ").strip().lower()
            
            # Check for F3 debug toggle
            if choice == 'f3':
                lives_manager.debug_mode = not lives_manager.debug_mode
                status = "enabled" if lives_manager.debug_mode else "disabled"
                print(f"\n🔧 Debug mode {status}")
                continue
            
            if choice != 'y':
                print("\nYou walk away alive. Wise choice.")
                break
    except KeyboardInterrupt:
        print("\n\nGame interrupted. You survive... for now.")


if __name__ == "__main__":
    main()
