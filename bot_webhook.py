from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = "https://unix-glass-bot-1.onrender.com"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# دستور /start
async def start(update: Update, context):
    await update.message.reply_text("ربات روشنه ✅")

application.add_handler(CommandHandler("start", start))

# مسیر وبهوک
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

if __name__ == "__main__":
    import asyncio

    async def run():
        # ست کردن وبهوک روی سرور شما
        await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()  # برای تست لوکال
        await asyncio.Event().wait()  # برنامه همیشه روشن بمونه

    asyncio.run(run())
