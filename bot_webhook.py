#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import threading
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, ContextTypes, filters
)

# ======= پیکربندی =======
TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = "https://unix-glass-bot-1.onrender.com"  # آدرس سرویس شما (بدون /TOKEN)

# ======= ثابت‌ها =======
GLUE_DATA = {
    "881": {"volume": 209, "weight": 284},
    "882": {"volume": 209, "weight": 319}
}

ENV, AREA, COUNT, THICKNESS, DEPTH, GLUE_CHOICE = range(6)

# ======= لاگینگ =======
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======= Flask WSGI app (نام متغیر باید "app" باشد تا gunicorn کار کند) =======
app = Flask(__name__)

# ======= تلگرام (Application و Bot) =======
bot = Bot(TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# ======= هندلرها =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("تکمیل اطلاعات", callback_data="fill_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "ربات روشنه ✅\nسلام ، به ربات هوشمند یونکس خوش آمدید\n"
        "جهت محاسبه متریال مصرفی شیشه دو جداره، اطلاعات را تکمیل کنید.",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "fill_info":
        await query.message.reply_text("1- محیط کل شیشه ها را وارد کنید (متر):")
        return ENV
    elif query.data in ("881", "882"):
        context.user_data["glue_choice"] = query.data
        await show_results(update, context)
        return ConversationHandler.END

async def get_env(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["env"] = float(update.message.text)
        await update.message.reply_text("2- مساحت شیشه ها را وارد کنید (مترمربع):")
        return AREA
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return ENV

async def get_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["area"] = float(update.message.text)
        await update.message.reply_text("3- تعداد کل شیشه ها را وارد کنید:")
        return COUNT
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return AREA

async def get_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["count"] = int(update.message.text)
        await update.message.reply_text("4- ضخامت اسپیسر را وارد کنید (میلیمتر):")
        return THICKNESS
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return COUNT

async def get_thickness(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["thickness"] = float(update.message.text)
        await update.message.reply_text("5- عمق چسب زنی را وارد کنید (میلیمتر):")
        return DEPTH
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return THICKNESS

async def get_depth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["depth"] = float(update.message.text)
        keyboard = [
            [InlineKeyboardButton("چسب 881", callback_data="881")],
            [InlineKeyboardButton("چسب 882", callback_data="882")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("چسب مصرفی خود را انتخاب کنید:", reply_markup=reply_markup)
        return GLUE_CHOICE
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return DEPTH

async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    env = data.get("env", 0.0)
    area = data.get("area", 0.0)
    count = data.get("count", 0)
    thickness = data.get("thickness", 0.0)
    depth = data.get("depth", 0.0)
    glue = data.get("glue_choice")

    # محاسبات
    volume_glue = (env * thickness * depth) / 1000
    glue_info = GLUE_DATA.get(glue, {"volume": 1, "weight": 0})
    weight_glue = (volume_glue / glue_info["volume"]) * glue_info["weight"]
    butyl = (env * 2 * 5.5) / 1000
    desiccant = (env * 3.5 * thickness) / 1000
    spacer = ((count * 4 * depth) / 100) - env

    # پاسخ به کاربر
    # ممکن است update یک CallbackQuery باشد؛ در نتیجه از callback_query.message استفاده می‌کنیم
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text(
        f"✅ نتایج محاسبه شده:\n"
        f"1- حجم چسب مصرفی: {volume_glue:.2f} لیتر\n"
        f"2- وزن چسب مصرفی: {weight_glue:.2f} کیلوگرم\n"
        f"3- بوتیل مصرفی: {butyl:.2f} کیلوگرم\n"
        f"4- رطوبت‌گیر مصرفی: {desiccant:.2f} کیلوگرم\n"
        f"5- اسپیسر مصرفی: {spacer:.2f} متر"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ عملیات لغو شد.")
    return ConversationHandler.END

# ======= Conversation Handler ثبت =======
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start), CallbackQueryHandler(button)],
    states={
        ENV: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_env)],
        AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_area)],
        COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_count)],
        THICKNESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_thickness)],
        DEPTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_depth)],
        GLUE_CHOICE: [CallbackQueryHandler(button, pattern="^(881|882)$")]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True
)
application.add_handler(conv_handler)

# ======= مسیر وبهوک (Flask) =======
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """دریافت آپدیت از تلگرام و قرار دادن آن در event loop برنامه تلگرام"""
    try:
        data = request.get_json(force=True)
    except Exception:
        return "bad request", 400

    update = Update.de_json(data, bot)

    # برنامه تلگرام در یک event-loop جدا در پس‌زمینه اجرا می‌شود.
    # اینجا آپدیت را به آن event-loop ارسال می‌کنیم.
    try:
        # async_loop توسط ترد راه‌اندازی می‌شود (پایین‌تر تعریف شده)
        asyncio.run_coroutine_threadsafe(application.process_update(update), async_loop)
    except Exception:
        logger.exception("Failed to schedule telegram update")
        # حتی اگر زمان‌بندی ناموفق باشد پاسخ 200 بده تا تلگرام دوباره ارسال نکند یا retry نکند
    return "OK"

# ======= راه‌اندازی application در یک event-loop جدا (برای gunicorn / render) =======
async_loop = None

async def _start_application_and_set_webhook():
    """ابتدا application را initialize و start می‌کنیم، سپس وبهوک را ست می‌کنیم."""
    await application.initialize()
    await application.start()
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    await application.bot.set_webhook(webhook_url)
    logger.info("Webhook set to: %s", webhook_url)
    # application در پس‌زمینه run شده و handlers آماده هستند.
    # این coroutine نیازی به توقف ندارد؛ event loop در ترد نگه داشته می‌شود.

def _start_async_loop_in_thread():
    global async_loop
    async_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(async_loop)
    # اجرای coroutine شروع اپلیکیشن (بدون بلاک کردن run_forever)
    async_loop.create_task(_start_application_and_set_webhook())
    async_loop.run_forever()

# ======= هنگام import (توسط gunicorn) ترد async را استارت می‌کنیم =======
threading.Thread(target=_start_async_loop_in_thread, daemon=True).start()

# ======= اجرا محلی وقتی با python bot_webhook.py اجرا می‌شود =======
if __name__ == "__main__":
    # اگر با python اجرا می‌کنید، یک ترد دیگر برای loop می‌سازیم (همان رفتار)
    # و سپس فلَس را در حالت توسعه اجرا می‌کنیم (برای تست محلی).
    if async_loop is None:
        threading.Thread(target=_start_async_loop_in_thread, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
