import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("7931935861:AAFtUmRlO0xakUJsu1qkjRzQJYgDErVhRp4")

# Flask serverni yaratish
app = Flask(__name__)

# Telegram bot ilovasi
application = Application.builder().token(TOKEN).build()

# /start komandasi uchun
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishga tushdi! /start buyrug'i qabul qilindi.")

# Bot admin qilinganda ishlaydigan funksiya
async def admin_promoted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = update.effective_chat.title
    await update.message.reply_text(
        f"✅ Bot ushbu guruhda admin qilindi!\n"
        f"🏷 Guruh nomi: {chat_title}\n"
        f"🆔 Guruh ID: {update.effective_chat.id}"
    )

# Xabarlarni o‘chirib tashlash
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.reply_to_message:
        try:
            await message.delete()
        except Exception as e:
            print(f"[ERROR] Xabar o‘chirilmadi: {e}")

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return "OK", 200

# Webhookni sozlash
def set_webhook():
    webhook_url = f"https://my-telegram-bot-uluh.onrender.com/{TOKEN}"  # URLingizni o‘rnating
    application.bot.setWebhook(webhook_url)

# Flask ilovasini ishga tushirish
if __name__ == "__main__":
    # Handlerlarni qo‘shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, admin_promoted))
    application.add_handler(MessageHandler(filters.REPLY, delete_messages))

    # Webhookni o‘rnatish
    set_webhook()

    # Flask serverni ishga tushirish
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
