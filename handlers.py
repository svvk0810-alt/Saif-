import os
import requests
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from downloader import VideoDownloader
from keyboards import (
    main_menu,
    quality_keyboard,
)

from utils import (
    is_url,
    format_duration,
    format_size,
)

from database import add_user

downloader = VideoDownloader()

USER_URLS = {}
USER_FORMATS = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    add_user(update.effective_user)

    text = f"""
🎬 مرحباً بك

📥 أرسل أي رابط فيديو.

يدعم:
• YouTube
• TikTok
• Facebook
• Instagram
• X
• وأكثر من 1000 موقع.

👨‍💻 المطور:
@saif_Officiel
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )
async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    if not is_url(url):

        await update.message.reply_text(
            "❌ أرسل رابطاً صحيحاً."
        )

        return

    try:

        info, formats = downloader.qualities(url)

    except Exception as e:

        await update.message.reply_text(
            f"❌ حدث خطأ\n\n{e}"
        )

        return

    USER_URLS[update.effective_user.id] = url

    USER_FORMATS[update.effective_user.id] = formats

    duration = format_duration(
        info.get("duration")
    )

    filesize = format_size(
        info.get("filesize")
    )

    title = info.get(
        "title",
        "بدون عنوان"
    )

    text = f"""
🎬 {title}

⏱️ {duration}

📦 {filesize}

اختر الجودة:
"""

    await update.message.reply_text(
        text,
        reply_markup=quality_keyboard(formats)
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id


    if user_id not in USER_URLS:

        await query.edit_message_text(
            "❌ أرسل رابط الفيديو أولاً."
        )

        return


    data = query.data

    url = USER_URLS[user_id]


    if data == "cancel":

        await query.edit_message_text(
            "❌ تم الإلغاء."
        )

        return


    await query.edit_message_text(
        "⏳ جاري تحميل الفيديو..."
    )


    try:

        # تحميل MP3
        if data == "audio":

            result = downloader.download_audio(
                url
            )

            file_path = result["file"]

            title = result.get(
                "title",
                "ملف صوتي"
            )


            await query.message.reply_audio(
                audio=open(file_path, "rb"),
                caption=f"🎵 {title}"
            )


        # تحميل فيديو
        else:

            quality = data.replace(
                "q_",
                ""
            )


            result = downloader.download_video(
                url,
                quality
            )


            file_path = result["file"]

            thumbnail = result.get(
                "thumbnail"
            )

            title = result.get(
                "title",
                "فيديو"
            )


            thumbnail_path = None


            # تحميل الصورة المصغرة
            if thumbnail:

                try:

                    thumbnail_path = "thumbnail.jpg"

                    response = requests.get(
                        thumbnail,
                        timeout=20
                    )

                    with open(
                        thumbnail_path,
                        "wb"
                    ) as f:

                        f.write(
                            response.content
                        )


                except Exception:

                    thumbnail_path = None



            await query.message.reply_video(
                video=open(file_path, "rb"),

                thumbnail=open(
                    thumbnail_path,
                    "rb"
                )
                if thumbnail_path
                else None,

                caption=f"✅ تم التحميل\n\n🎬 {title}"
            )


            # حذف الصورة المؤقتة
            if thumbnail_path and os.path.exists(
                thumbnail_path
            ):

                os.remove(
                    thumbnail_path
                )



        # حذف الفيديو بعد الإرسال
        if os.path.exists(file_path):

            os.remove(
                file_path
            )


    except Exception as e:

        await query.message.reply_text(
            f"❌ حدث خطأ:\n{e}"
        )