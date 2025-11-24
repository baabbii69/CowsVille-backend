#!/usr/bin/env python3
"""
Health check script for Cowsville application.
Checks if the application is responding and restarts if needed.
"""
import os
import pathlib

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment or defaults
HEALTH_URL = os.getenv("HEALTH_CHECK_URL", "http://127.0.0.1:8000/health/")
RESTART_FILE = pathlib.Path(
    os.getenv("RESTART_FILE_PATH", "/root/CowsVille-backend/tmp/restart.txt")
)

# Ensure restart file directory exists
RESTART_FILE.parent.mkdir(parents=True, exist_ok=True)

try:
    r = requests.get(HEALTH_URL, timeout=5)
    if r.status_code != 200:
        print(f"Health check failed with status {r.status_code}, touching restart file")
        RESTART_FILE.touch()
except Exception as e:
    print(f"Health check exception: {e}, touching restart file")
    RESTART_FILE.touch()
