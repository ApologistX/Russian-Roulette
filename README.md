# Russian Roulette (CLI Game)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A terminal-based Python implementation of Russian Roulette. The game simulates a six-chamber revolver, complete with an animated cylinder spin and a permanent “death state.” Once the player dies, a hidden death marker file is written to the system’s configuration directory, preventing further gameplay unless manually deleted.

---

## Features
- 1-in-6 randomized chamber (true Russian Roulette simulation)
- Permanent death tracked via a hidden `.death_marker` file
- Animated ASCII spinning sequence
- Cross-platform support:
  - **Windows:** `%LOCALAPPDATA%\.roulette\.death_marker`
  - **Linux/macOS:** `~/.config/roulette/.death_marker`
- Infinite play until a fatal chamber is hit
- No external dependencies

---

## Death File Behavior
When you die, the game writes:

**Windows**
%LOCALAPPDATA%.roulette.death_marker

**Linux / macOS**
~/.config/roulette/.death_marker


If this file exists, the game refuses to run.  
Delete it manually to reset your status.

---

## Installation
```bash
git clone https://github.com/ApologistX/Russian-Roulette
cd russian-roulette
python3 roulette.py
```
## Gameplay Summary

1. At launch, the game checks for the `.death_marker` file.  
   - If it exists, the game immediately exits and cannot be played again.

2. Press ENTER to spin the cylinder.  
   An ASCII animation sequence simulates the revolver spinning.

3. Press ENTER to pull the trigger.

4. If the chamber is empty, you survive the round and may continue playing.

5. If the chamber contains the bullet, you die permanently.  
   The game writes `.death_marker` to your system, preventing all future play until manually deleted.

## Resetting the Game

To reset your death state and play again, manually delete the `.death_marker` file created when you die.

**Linux / macOS**
```bash
rm ~/.config/roulette/.death_marker
```

**Windows (PowerShell)**
```bash
Remove-Item "$env:LOCALAPPDATA\.roulette\.death_marker"
```

