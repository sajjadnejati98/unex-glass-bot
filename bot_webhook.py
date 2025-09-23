import os
import asyncio
from threading import Thread
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = f"https://unix-glass-bot-1.onrender.com/{TOKEN}"  # دامنه شما جایگذاری شد

app = Flask(__name__)
bot = Bot(TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# دستور /start
async def start(update: Update, context):
    await update.message.reply_text("ربات فعال شد!")

application.add_handler(CommandHandler("start", start))

# وبهوک
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    application.update_queue.put(update)
    return "ok"

# اجرای Flask در یک thread جداگانه
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

async def main():
    # ست کردن وبهوک
    await application.bot.set_webhook(WEBHOOK_URL)
    # اجرای Flask
    Thread(target=run_flask).start()
    # اجرای اپلیکیشن تلگرام
    await application.initialize()
    await application.start()
    await application.updater.stop()  # چون فقط وبهوک استفاده می‌کنیم
    await application.idle()

if __name__ == "__main__":
    asyncio.run(main())
