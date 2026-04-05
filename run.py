#!/usr/bin/env python3
"""
Sentinel-Scribe Main Entry Point
Run from root directory: python run.py [options]
"""

import sys
import os

# Ensure we can import from sentinel_scribe
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sentinel_scribe'))

from cli import main

if __name__ == "__main__":
    sys.exit(main())
