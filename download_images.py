#!/usr/bin/env python3
"""
Main entry point for the Image Downloader tool
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.image_downloader.cli import main

if __name__ == '__main__':
    main() 