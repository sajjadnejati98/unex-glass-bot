from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = "https://unix-glass-bot-1.onrender.com/webhook"

app = Flask(__name__)
bot = Bot(token=TOKEN)

# ApplicationBuilder جایگزین Dispatcher شده
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("سلام! ربات فعال شد ✅")

async def echo(update: Update, context):
    await update.message.reply_text(f"پیام شما: {update.message.text}")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

if __name__ == "__main__":
    import asyncio
    asyncio.run(bot.delete_webhook())
    asyncio.run(bot.set_webhook(WEBHOOK_URL))
    print(f"Webhook ست شد: {WEBHOOK_URL}")
    print("ربات آماده روی پورت 5000")
    app.run(host="0.0.0.0", port=5000)
