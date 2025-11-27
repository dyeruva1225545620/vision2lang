"""
Hugging Face Spaces entry point for Vision2Lang
This file imports and runs the main app from src/
"""

import sys
import os

# Add src directory to path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
from app import main

if __name__ == "__main__":
    main()

