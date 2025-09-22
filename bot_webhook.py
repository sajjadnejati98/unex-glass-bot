# bot_webhook.py
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_PATH = "/webhook"

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
bot = Bot(TOKEN)

# ======= دستورات ربات =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("تکمیل اطلاعات", callback_data="fill_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "سلام! ربات یونکس فعال است.\nجهت محاسبه متریال مصرفی دکمه را بزنید.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"شما دکمه {query.data} را زدید.")

# ======= اپلیکیشن تلگرام =======
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))

# ======= وبهوک =======
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    application.update_queue.put_nowait(update)
    return "OK"

# ======= اجرا =======
if __name__ == "__main__":
    # روی Render با gunicorn اجرا شود:
    # gunicorn bot_webhook:app
    app.run(host="0.0.0.0", port=5000)
