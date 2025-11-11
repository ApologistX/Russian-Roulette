#!/usr/bin/env python3
"""
Russian Roulette - A simulated game of chance
The game tracks "deaths" permanently via a hidden config file.
"""

import os
import random
import sys
import platform
import time
from pathlib import Path


def get_death_file_path():
    """Get the path to the death marker file based on OS"""
    if platform.system() == "Windows":
        base_path = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~')))
        config_dir = base_path / '.roulette'
    else:  # Linux, macOS, etc.
        config_dir = Path.home() / '.config' / 'roulette'
    
    # Create directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / '.death_marker'


def is_dead():
    death_file = get_death_file_path()
    return death_file.exists()


def mark_dead():
    death_file = get_death_file_path()
    with open(death_file, 'w') as f:
        f.write("DEAD\n")


def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def spin_cylinder():
    frames = [
        """
                                    LIVELIVELIVELIVELIVELIVELIVELIV                                                    
                                  ELI                             VELIV                             
                                ELI                                 VEL                             
                               IVE                                    LIV                           
                             ELIV      EVILEVI          LEVILEV       LIVE                         
                             LI        VELIVEL          IVELIVE          LI                         
                             VE        LIVELIV          ELIVELI          VE                         
                             LI        VELIVEL          IVELIVE          LI                         
                             VE                                          LI                         
                             VE                                          LI                         
                             VE  LIVE                            LIVE    LI                         
                             VE  LIVE                           LIVE     AC                         
                               ZS  KAL                          SAH   ZW AC                         
                            SDDSD   XWNDK                      QDJWX   XDFWW                         
                             ADSD    XUNDJ                  PFJUW   XFIWW                           
                              ZXCC     XSPGGGH            PGKSV     XAE                             
                               YZQJS     YTTTQGGGGGGGGGGGGNTW     WGJTU                             
                                 VSOIS       YTTTTTTTTTTTTX     VINSU                               
                                   WSPKTNR                  TKKJNSU                                 
                                     VUURQKLLN          RLKKNQQRU                                   
                                         XPPPQLLLLLLLLLLPQPPU                                       
                                             YOOOOOOOOOOW                             
        """,
        """
                                        DIEDIEDIEDIEDIEDIEDIE                                        
                                    DIEDIEDIEDIEDIEDIEDIEDIEDIE                                    
                                DIEDIEDIE                  DIEDIEDIE                                 
                              DIEDIE                           DIEDIE                               
                            DIEDI                                 EDIE                             
                            DIE                                     DIE                             
                          DIEIE                                     DIEIE                           
                          DIE                                         DIE                           
                        DIEIE                                         DIEIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE         DIEDIEDI           DIEDIEDIE        DIE                         
                        DIE         DIEDIEDI           DIEDIEDIE        DIE                         
                        DIE                                             DIE                         
                        DIE                DIEDIEDIEDIED                DIE                         
                        PNKLV           DIEDIEDIEDIEDIEDIE            XLLNP                         
                          FAS           DIEDIE       DIEDI            VAE                           
                          ROKJW         DIED           DIE          WJKOQ                           
                            FAU                                     UAE                             
                            TRKIW                                 VIKRS                             
                              RQJHHHY                          JHHLQS                               
                                SRRRGHHHU                  LHHHORRU                                 
                                    RQQSJHHHHHHHHHHHHHHHHHHOQQQY                                    
                                        SRRRRRRRRRRRRRRRRRRY                
        """,
        """
                                    LIVELIVELIVELIVELIVELIVELIVELIV                                                    
                                  ELI                             VELIV                             
                                ELI                                 VEL                             
                               IVE                                    LIV                           
                             ELIV      EVILEVI          LEVILEV       LIVE                         
                             LI        VELIVEL          IVELIVE          LI                         
                             VE        LIVELIV          ELIVELI          VE                         
                             LI        VELIVEL          IVELIVE          LI                         
                             VE                                          LI                         
                             VE                                          LI                         
                             VE  LIVE                            LIVE    LI                         
                             VE  LIVE                           LIVE     AC                         
                               ZS  KAL                          SAH   ZW AC                         
                            SDDSD   XWNDK                      QDJWX   XDFWW                         
                             ADSD    XUNDJ                  PFJUW   XFIWW                           
                              ZXCC     XSPGGGH            PGKSV     XAE                             
                               YZQJS     YTTTQGGGGGGGGGGGGNTW     WGJTU                             
                                 VSOIS       YTTTTTTTTTTTTX     VINSU                               
                                   WSPKTNR                  TKKJNSU                                 
                                     VUURQKLLN          RLKKNQQRU                                   
                                         XPPPQLLLLLLLLLLPQPPU                                       
                                             YOOOOOOOOOOW                    
        """,
        """
                                        DIEDIEDIEDIEDIEDIEDIE                                        
                                    DIEDIEDIEDIEDIEDIEDIEDIEDIE                                    
                                DIEDIEDIE                  DIEDIEDIE                                 
                              DIEDIE                           DIEDIE                               
                            DIEDI                                 EDIE                             
                            DIE                                     DIE                             
                          DIEIE                                     DIEIE                           
                          DIE                                         DIE                           
                        DIEIE                                         DIEIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE         DIEDIEDI           DIEDIEDIE        DIE                         
                        DIE         DIEDIEDI           DIEDIEDIE        DIE                         
                        DIE                                             DIE                         
                        DIE                DIEDIEDIEDIED                DIE                         
                        PNKLV           DIEDIEDIEDIEDIEDIE            XLLNP                         
                          FAS           DIEDIE       DIEDI            VAE                           
                          ROKJW         DIED           DIE          WJKOQ                           
                            FAU                                     UAE                             
                            TRKIW                                 VIKRS                             
                              RQJHHHY                          JHHLQS                               
                                SRRRGHHHU                  LHHHORRU                                 
                                    RQQSJHHHHHHHHHHHHHHHHHHOQQQY                                    
                                        SRRRRRRRRRRRRRRRRRRY 
        """,
        """
                                    LIVELIVELIVELIVELIVELIVELIVELIV                                                    
                                  ELI                             VELIV                             
                                ELI                                 VEL                             
                               IVE                                    LIV                           
                             ELIV      EVILEVI          LEVILEV       LIVE                         
                             LI        VELIVEL          IVELIVE          LI                         
                             VE        LIVELIV          ELIVELI          VE                         
                             LI        VELIVEL          IVELIVE          LI                         
                             VE                                          LI                         
                             VE                                          LI                         
                             VE  LIVE                            LIVE    LI                         
                             VE  LIVE                           LIVE     AC                         
                               ZS  KAL                          SAH   ZW AC                         
                            SDDSD   XWNDK                      QDJWX   XDFWW                         
                             ADSD    XUNDJ                  PFJUW   XFIWW                           
                              ZXCC     XSPGGGH            PGKSV     XAE                             
                               YZQJS     YTTTQGGGGGGGGGGGGNTW     WGJTU                             
                                 VSOIS       YTTTTTTTTTTTTX     VINSU                               
                                   WSPKTNR                  TKKJNSU                                 
                                     VUURQKLLN          RLKKNQQRU                                   
                                         XPPPQLLLLLLLLLLPQPPU                                       
                                             YOOOOOOOOOOW                    
        """,
        """
                                        DIEDIEDIEDIEDIEDIEDIE                                        
                                    DIEDIEDIEDIEDIEDIEDIEDIEDIE                                    
                                DIEDIEDIE                  DIEDIEDIE                                 
                              DIEDIE                           DIEDIE                               
                            DIEDI                                 EDIE                             
                            DIE                                     DIE                             
                          DIEIE                                     DIEIE                           
                          DIE                                         DIE                           
                        DIEIE                                         DIEIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE                                             DIE                         
                        DIE         DIEDIEDI           DIEDIEDIE        DIE                         
                        DIE         DIEDIEDI           DIEDIEDIE        DIE                         
                        DIE                                             DIE                         
                        DIE                DIEDIEDIEDIED                DIE                         
                        PNKLV           DIEDIEDIEDIEDIEDIE            XLLNP                         
                          FAS           DIEDIE       DIEDI            VAE                           
                          ROKJW         DIED           DIE          WJKOQ                           
                            FAU                                     UAE                             
                            TRKIW                                 VIKRS                             
                              RQJHHHY                          JHHLQS                               
                                SRRRGHHHU                  LHHHORRU                                 
                                    RQQSJHHHHHHHHHHHHHHHHHHOQQQY                                    
                                        SRRRRRRRRRRRRRRRRRRY 
        """
    ]
    
    print("\n Spinning the cylinder...\n")
    
    # Spin animation
    for _ in range(12):
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
        mark_dead()
        return False
    else:
        print("✓ You survived this round!")
        print(f"Chamber {chamber}/6 was empty.")
        return True


def main():
    """Main game loop"""
    # Check if player is already dead
    if is_dead():
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
