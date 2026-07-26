import os
import re
import math
from config import DOWNLOADS_DIR

URL_PATTERN = re.compile(
    r"(https?://[^\s]+)"
)

def is_url(text: str) -> bool:
    if not text:
        return False
    return bool(URL_PATTERN.search(text))


def format_size(size):
    if not size:
        return "غير معروف"

    power = 1024
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]

    while size >= power and n < len(units) - 1:
        size /= power
        n += 1

    return f"{size:.2f} {units[n]}"


def format_duration(seconds):
    if not seconds:
        return "00:00"

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    if h:
        return f"{h:02}:{m:02}:{s:02}"

    return f"{m:02}:{s:02}"


def sanitize_filename(name):
    invalid = '<>:"/\\|?*'

    for c in invalid:
        name = name.replace(c, "_")

    return name


def ensure_download_folder():
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)


def delete_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
    except:
        pass

    return False


def progress_bar(percent):

    percent = int(percent)

    filled = math.floor(percent / 10)

    empty = 10 - filled

    return "🟩" * filled + "⬜" * empty