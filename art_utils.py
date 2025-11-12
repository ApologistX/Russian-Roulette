#!/usr/bin/env python3
"""
Utility functions for art-related operations.
"""

class Art:
    """Class to load and store ASCII art from text files."""
    def __init__(self, directory: str):
        try:
            with open(directory + "/Alive.txt", 'r') as file:
                self.Alive = file.read()
            with open(directory + "/Dead.txt", 'r') as file:
                self.Dead = file.read()
        except FileNotFoundError as e:
            print(f"Error loading art files: {e}")
            self.Alive = ""
            self.Dead = ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.Alive = ""
            self.Dead = ""