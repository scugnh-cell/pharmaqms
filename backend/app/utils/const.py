import os
import platform

current_dir = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(current_dir, "..", ".."))
PROJECT_DIR = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
LOG_DIR = os.path.join(PROJECT_DIR, "logs")

for d in [DATA_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

IN_WINDOWS = platform.system() == "Windows"
