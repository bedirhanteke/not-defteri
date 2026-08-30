#!/usr/bin/env python3
import sys
import os

# Add current dir to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == '__main__':
    sys.exit(main())
