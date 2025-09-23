import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"
PORT = int(__import__("os").environ.get("PORT", 5000))
HOST = __import__("os").environ.get("RENDER_EXTERNAL_HOSTNAME")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات فعال است ✅")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.bot.set_webhook(f"https://{HOST}/{TOKEN}")
    # اجرای ربات روی وبهوک
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_path=f"/{TOKEN}"
    )

if __name__ == "__main__":
    asyncio.run(main())
