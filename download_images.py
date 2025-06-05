#!/usr/bin/env python3
"""
Main entry point for the Image Downloader tool
"""
import sys
import os
from tools.cli import main

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    main() 