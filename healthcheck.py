#!/usr/bin/env python3
import pathlib

import requests

HEALTH_URL = "https://apiv3.cowsville-aau-cvma.com/health/"
RESTART_FILE = pathlib.Path("/home/cowsvijp/apiv3/tmp/restart.txt")

try:
    r = requests.get(HEALTH_URL, timeout=5)
    if r.status_code != 200:
        RESTART_FILE.touch()
except Exception:
    RESTART_FILE.touch()
