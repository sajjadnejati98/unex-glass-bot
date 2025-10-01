import logging
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, ContextTypes, filters
)

# ======= تنظیمات =======
TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = "https://unex-glass-bot.onrender.com"

GLUE_DATA = {
    "881": {"volume": 209, "weight": 284},
    "882": {"volume": 209, "weight": 319}
}

ENV, AREA, COUNT, THICKNESS, DEPTH, GLUE_CHOICE = range(6)

# ======= لاگینگ =======
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======= Flask App =======
app_flask = Flask(__name__)

# ======= Telegram Bot و Application =======
bot = Bot(TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# ======= Handlers =======

# ... (همان توابع start, button, get_env, ..., cancel بدون تغییر) ...

# ======= Conversation Handler =======

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        CallbackQueryHandler(button, pattern='^fill_info$')
    ],
    states={
        ENV: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_env)],
        AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_area)],
        COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_count)],
        THICKNESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_thickness)],
        DEPTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_depth)],
        GLUE_CHOICE: [CallbackQueryHandler(button, pattern='^(881|882)$')]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
)

application.add_handler(conv_handler)

# ======= Flask Routes =======

@app_flask.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return "OK"

@app_flask.route("/", methods=["GET"])
def home():
    return "Unix Glass Bot is running! ✅"

# ======= فعال‌سازی application در اولین درخواست =======

_started = False

@app_flask.before_request
def setup_application():
    global _started
    if not _started:
        import threading
        def run_app():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(application.initialize())
            loop.run_until_complete(application.start())
        threading.Thread(target=run_app, daemon=True).start()
        _started = True
