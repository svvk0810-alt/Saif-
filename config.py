# ===========================================
# Saif Video Downloader Bot
# Developer: Saif (@saif_Officiel)
# ===========================================

import os

# ضع توكن البوت هنا
BOT_TOKEN = "8848324448:AAFUtv6seGAb5gAtkGxBbWIVXNVnLuVrZPI"

# معرف المطور
DEVELOPER_NAME = "سيف"
DEVELOPER_USERNAME = "@saif_Officiel"

# المجلدات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# اللغات
DEFAULT_LANGUAGE = "ar"

# أقصى عدد تحميلات بنفس الوقت
MAX_CONCURRENT_DOWNLOADS = 3

# حذف الملفات بعد الإرسال
AUTO_DELETE_FILES = True

# دعم المواقع بواسطة yt-dlp
SUPPORTED_SITES = "1000+"

# إعدادات yt-dlp
YTDLP_OPTIONS = {
    "quiet": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "no_warnings": True,
    "restrictfilenames": False,
}