import os
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from flask import Flask, request

TOKEN = os.getenv("TOKEN")  # حتماً توکنت رو از محیط بذار
if not TOKEN:
    raise ValueError("توکن ربات خالیه!")

app = Flask(__name__)
bot = Bot(TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

async def start(update, context):
    await update.message.reply_text("ربات فعال شد!")

application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = telegram.Update.de_json(data, bot)
    application.update_queue.put(update)
    return "ok"

if __name__ == "__main__":
    # webhook URL باید واقعی باشه
    webhook_url = f"https://YOUR_DOMAIN/{TOKEN}"
    application.bot.set_webhook(webhook_url)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
