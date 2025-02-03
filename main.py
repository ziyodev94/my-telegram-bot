import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, Dispatcher

# Telegram Token (Render.com Environment Variables orqali olish)
TOKEN = os.getenv("7931935861:AAFtUmRlO0xakUJsu1qkjRzQJYgDErVhRp4")

# Flask ilovasini yaratamiz
app = Flask(__name__)

# Telegram bot va Dispatcher
application = Application.builder().token(TOKEN).build()
dp = Dispatcher(application.bot, None, use_context=True)

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start komandasi uchun
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishga tushdi! /start buyrug'i qabul qilindi.")

# Bot admin qilinganda ishlaydigan funktsiya
async def admin_promoted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = update.effective_chat.title
    await update.message.reply_text(
        f"✅ Bot ushbu guruhda admin qilindi!\n"
        f"🏷 Guruh nomi: {chat_title}\n"
        f"🆔 Guruh ID: {update.effective_chat.id}"
    )
    logger.info(f"[LOGGING] Bot {chat_title} guruhida admin qilindi!")

# Xabarlarni o'chirganda log qilish
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.reply_to_message:
        try:
            await message.delete()
            logger.info(
                f"[DELETED] Xabar o'chirildi!\n"
                f"User: @{message.from_user.username}\n"
                f"Guruh: {message.chat.title}\n"
                f"Xabar ID: {message.message_id}\n"
                "--------------------------"
            )
        except Exception as e:
            logger.error(f"[ERROR] Xabar o'chirilmadi: {e}")

# Webhook uchun Flask route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    dp.process_update(update)
    return "OK", 200

# Webhookni sozlash
def set_webhook():
    webhook_url = f"https://your-render-url.onrender.com/{TOKEN}"  # Render.com URL-ni qo'shing
    application.bot.setWebhook(webhook_url)
    logger.info(f"Webhook set to {webhook_url}")

# Botni ishga tushirish
if __name__ == "__main__":
    # Handlerlarni qo‘shamiz
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, admin_promoted))
    dp.add_handler(MessageHandler(filters.REPLY, delete_messages))

    # Webhookni sozlash
    set_webhook()

    # Flask ilovasini ishga tushirish
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

