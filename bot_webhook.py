import os
import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
if not TOKEN:
    raise ValueError("توکن ربات خالیه!")

app = Flask(__name__)
bot = Bot(TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# دستورات ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات فعال شد!")

application.add_handler(CommandHandler("start", start))

# وبهوک
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    application.update_queue.put_nowait(update)
    return "ok"

async def main():
    webhook_url = f"https://unix-glass-bot-1.onrender.com/{TOKEN}"
    await application.bot.set_webhook(webhook_url)
    # اجرای Flask داخل asyncio
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = [f"0.0.0.0:{os.environ.get('PORT', 5000)}"]
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())
