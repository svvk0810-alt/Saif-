from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import DEVELOPER_USERNAME


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📥 تحميل فيديو", callback_data="download")
        ],
        [
            InlineKeyboardButton("ℹ️ المساعدة", callback_data="help"),
            InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{DEVELOPER_USERNAME.replace('@','')}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def quality_keyboard(formats):

    keyboard = []

    # عرض أفضل 8 جودات فقط
    for quality in formats[:8]:

        keyboard.append([
            InlineKeyboardButton(
                quality["text"],
                callback_data=f"q_{quality['id']}"
            )
        ])


    keyboard.append([
        InlineKeyboardButton(
            "🎵 MP3",
            callback_data="audio"
        )
    ])


    keyboard.append([
        InlineKeyboardButton(
            "❌ إلغاء",
            callback_data="cancel"
        )
    ])


    return InlineKeyboardMarkup(keyboard)

    return InlineKeyboardMarkup(keyboard)


def cancel_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "❌ إلغاء التحميل",
                callback_data="cancel"
            )
        ]
    ])