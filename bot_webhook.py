from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات فعال است ✅")

if __name__ == "__main__":
    # ساخت اپلیکیشن
    app = ApplicationBuilder().token(TOKEN).build()

    # اضافه کردن دستور /start
    app.add_handler(CommandHandler("start", start))

    # اجرای وبهوک
    webhook_url = f"https://unix-glass-bot-1.onrender.com/{TOKEN}"
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=webhook_url
    )
