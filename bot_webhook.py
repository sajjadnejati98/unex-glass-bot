from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ======== تنظیمات نهایی ========
TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = "https://unix-glass-bot-1.onrender.com/webhook"
PORT = 5000
# =============================

app = Flask(__name__)
bot = Bot(token=TOKEN)

# ایجاد Application PTB v20.3
application = Application.builder().token(TOKEN).build()

# ======== دستورات ربات ========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات یونکس فعال شد!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"پیام شما: {update.message.text}")
# ==============================

# افزودن Handler ها
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ======== وبهوک Flask ========
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return "OK", 200

# ======== اجرای ربات ========
if __name__ == "__main__":
    # ست کردن وبهوک یکبار برای همیشه
    bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook ست شد: {WEBHOOK_URL}")
    print(f"ربات آماده روی پورت {PORT}")
    app.run(host="0.0.0.0", port=PORT)
