import os
from datetime import datetime
import glob


LOG_FILE = "./logs/processing.log"
MODEL_DIR = "./models/"
DATA_DIR = "./data/"
MAP_FOLDER = './map_data/'
MATRIX_FOLDER = './matrix_data/'


def log_message(message):
    """Appends a log message with a timestamp to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
        
def get_latest_file(folder, pattern, ext):
    """Return the path to the most recent file matching the pattern."""
    file_pattern = f'{folder}/{pattern}*.{ext}'
    all_files = glob.glob(file_pattern)
    if not all_files:
        log_message(f"No files found matching pattern: {file_pattern}")
        return None
    
    return max(all_files, key=os.path.getmtime).replace('\\', '/')

