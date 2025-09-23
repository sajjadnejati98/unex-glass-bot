from flask import Flask, request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)
import asyncio

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = "https://unix-glass-bot-1.onrender.com"

ENV, AREA, COUNT, THICKNESS, DEPTH, GLUE_CHOICE = range(6)
GLUE_DATA = {"881": {"volume":209, "weight":284}, "882":{"volume":209, "weight":319}}

app = Flask(__name__)
bot = Bot(TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Handlers مشابه کد شما ...

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "ربات روشن است ✅"

async def main():
    await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    await application.initialize()
    await application.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
