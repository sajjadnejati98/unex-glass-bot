from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = "https://unix-glass-bot-1.onrender.com/webhook"

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

def start(update, context):
    update.message.reply_text("سلام! ربات فعال شد ✅")

def echo(update, context):
    update.message.reply_text(f"پیام شما: {update.message.text}")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook ست شد: {WEBHOOK_URL}")
    print("ربات آماده روی پورت 5000")
    app.run(host="0.0.0.0", port=5000)
