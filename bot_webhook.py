#!/usr/bin/env python3
import asyncio
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, ContextTypes, filters
)

# ======= توکن ربات =======
TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
WEBHOOK_URL = "https://unix-glass-bot-1.onrender.com"

# ======= ثابت‌ها =======
GLUE_DATA = {
    "881": {"volume": 209, "weight": 284},
    "882": {"volume": 209, "weight": 319}
}

ENV, AREA, COUNT, THICKNESS, DEPTH, GLUE_CHOICE = range(6)

# ======= Logging =======
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======= Flask App =======
app_flask = Flask(__name__)
bot = Bot(TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# ======= Handlers =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("تکمیل اطلاعات", callback_data='fill_info')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "ربات روشنه ✅\nسلام ، به ربات هوشمند یونکس خوش آمدید\n"
        "جهت محاسبه متریال مصرفی شیشه دو جداره، اطلاعات را تکمیل کنید.",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'fill_info':
        await query.message.reply_text("1- محیط کل شیشه ها را وارد کنید (متر):")
        return ENV
    elif query.data in ["881", "882"]:
        context.user_data['glue_choice'] = query.data
        await show_results(update, context)
        return ConversationHandler.END

async def get_env(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['env'] = float(update.message.text)
        await update.message.reply_text("2- مساحت شیشه ها را وارد کنید (مترمربع):")
        return AREA
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return ENV

async def get_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['area'] = float(update.message.text)
        await update.message.reply_text("3- تعداد کل شیشه ها را وارد کنید:")
        return COUNT
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return AREA

async def get_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['count'] = int(update.message.text)
        await update.message.reply_text("4- ضخامت اسپیسر را وارد کنید (میلیمتر):")
        return THICKNESS
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return COUNT

async def get_thickness(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['thickness'] = float(update.message.text)
        await update.message.reply_text("5- عمق چسب زنی را وارد کنید (میلیمتر):")
        return DEPTH
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return THICKNESS

async def get_depth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['depth'] = float(update.message.text)
        keyboard = [
            [InlineKeyboardButton("چسب 881", callback_data='881')],
            [InlineKeyboardButton("چسب 882", callback_data='882')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("چسب مصرفی خود را انتخاب کنید:", reply_markup=reply_markup)
        return GLUE_CHOICE
    except ValueError:
        await update.message.reply_text("لطفاً عدد معتبر وارد کنید.")
        return DEPTH

async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    env = data['env']
    area = data['area']
    count = data['count']
    thickness = data['thickness']
    depth = data['depth']
    glue = data['glue_choice']

    volume_glue = (env * thickness * depth) / 1000
    glue_info = GLUE_DATA[glue]
    weight_glue = (volume_glue / glue_info['volume']) * glue_info['weight']
    butyl = (env * 2 * 5.5) / 1000
    desiccant = (env * 3.5 * thickness) / 1000
    spacer = ((count * 4 * depth) / 100) - env

    await update.callback_query.message.reply_text(
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

# ======= Conversation Handler =======
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start), CallbackQueryHandler(button)],
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

# ======= Flask Webhook Route =======
@app_flask.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return "OK"

# ======= اجرای همزمان Flask و تلگرام =======
if __name__ == "__main__":
    async def main():
        await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
        await application.initialize()
        await application.start()
        await asyncio.gather(
            application.updater.start_polling(),
            asyncio.to_thread(lambda: app_flask.run(host="0.0.0.0", port=5000))
        )
        await asyncio.Event().wait()

    asyncio.run(main())
