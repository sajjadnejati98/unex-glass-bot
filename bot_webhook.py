from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import os

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

# دستورات ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات فعال است ✅")

# ساخت اپلیکیشن تلگرام
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# وبهوک Flask
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

# روت ساده
@app.route("/")
def index():
    return "ربات فعال است ✅", 200

if __name__ == "__main__":
    # ست کردن وبهوک
    application.bot.set_webhook(f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
    # اجرا روی پورت داینامیک Render
    app.run(host="0.0.0.0", port=PORT)
