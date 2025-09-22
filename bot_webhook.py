from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_PATH = "/webhook"

app = Flask(__name__)
bot = Bot(TOKEN)

# ======= هندلر /start =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات یونکس فعال است.")

# ======= هندلر پیام ناشناخته =======
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دستور نامشخص. لطفاً از /start استفاده کن.")

# ======= Application =======
app_telegram = ApplicationBuilder().token(TOKEN).build()
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown))

# ======= وبهوک =======
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await app_telegram.process_update(update)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
