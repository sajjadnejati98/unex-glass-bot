from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler
from flask import Flask, request

# توکن ربات شما
TOKEN = "8208186251:AAGhImACKTeAa1pKT1cVSQEsqp0Vo2yk-2o"

app = Flask(__name__)
bot = Bot(TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("ربات فعال شد!")

application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    application.update_queue.put(update)
    return "ok"

if __name__ == "__main__":
    # آدرس وبهوک واقعی خودتون رو اینجا بذارید
    webhook_url = f"https://YOUR_DOMAIN/{TOKEN}"
    application.bot.set_webhook(webhook_url)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
