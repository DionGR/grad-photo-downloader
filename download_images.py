#!/usr/bin/env python3
"""
Main entry point for the Image Downloader tool
"""
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


import sys
import os
from tools.cli import main

if __name__ == '__main__':
    main() 