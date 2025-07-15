from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / 'logs'
LOCKS_DIR = BASE_DIR / 'locks'
BIN_DIR = BASE_DIR / 'bin'
