from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import BOT_TOKEN
from database import setup

from handlers import (
    start,
    receive_link,
    button_callback,
)


def main():

    # إنشاء قاعدة البيانات
    setup()


    # إنشاء التطبيق مع مهلات اتصال أكبر
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(60)
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .build()
    )


    # أمر /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # أزرار الجودة
    app.add_handler(
        CallbackQueryHandler(
            button_callback
        )
    )


    # استقبال الروابط
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_link
        )
    )


    print("====================================")
    print("Bot Started Successfully")
    print("====================================")


    # تشغيل البوت
    app.run_polling(
        allowed_updates=[
            "message",
            "callback_query"
        ]
    )



if __name__ == "__main__":
    main()