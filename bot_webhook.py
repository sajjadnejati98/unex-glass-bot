import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request

# -----------------------
# تنظیمات ربات
# -----------------------
TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = f"https://unix-glass-bot-1.onrender.com/{TOKEN}"

if not TOKEN:
    raise ValueError("توکن ربات خالیه!")

# -----------------------
# Flask App
# -----------------------
app = Flask(__name__)

# -----------------------
# Telegram Bot
# -----------------------
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات فعال شد!")

application.add_handler(CommandHandler("start", start))

# -----------------------
# Webhook Route
# -----------------------
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return "ok"

# -----------------------
# ست کردن وبهوک
# -----------------------
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    asyncio.run(set_webhook())
