#!/usr/bin/env python3
"""
penina_launcher.py

Standalone launcher for the Penina PDF417 Scanner & Encoder application.
This file serves as the entry point for the Windows executable to avoid
relative import issues in PyInstaller.

Author: Erick Ochieng Opiyo
Email: opiyoerick08@gmail.com
GitHub: https://github.com/alphonsi
"""

import sys
import os

# Add the penina package to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
penina_dir = os.path.join(current_dir, 'penina')
sys.path.insert(0, current_dir)

# Import the main application
from penina.main import main

if __name__ == "__main__":
    main()