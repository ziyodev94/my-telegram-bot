from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN  # Tokenni config.py orqali olamiz

# /start komandasi uchun
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishga tushdi janob! /start buyrug'i qabul qilindi.")

# Bot admin qilinganda ishlaydigan funktsiya
async def admin_promoted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = update.effective_chat.title
    await update.message.reply_text(
        f"✅ Bot ushbu guruhda admin qilindi!\n"
        f"🏷 Guruh nomi: {chat_title}\n"
        f"🆔 Guruh ID: {update.effective_chat.id}"
    )
    print(f"[LOGGING] Bot {chat_title} guruhida admin qilindi!")

# Xabarlarni o‘chirganda log qilish
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    # Faqat reply xabarlarni o'chiramiz
    if message.reply_to_message:
        try:
            await message.delete()
            # Log qismi
            print(
                f"[DELETED] Xabar o'chirildi!\n"
                f"User: @{message.from_user.username}\n"
                f"Guruh: {message.chat.title}\n"
                f"Xabar ID: {message.message_id}\n"
                "--------------------------"
            )
        except Exception as e:
            print(f"[ERROR] Xabar o‘chirilmadi: {e}")

# Oddiy foydalanuvchilar yuborgan buyruqlarni o‘chirish
async def delete_user_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.text and message.text.startswith("/") and not message.from_user.is_bot:
        try:
            await message.delete()
            print(f"[DELETED] Foydalanuvchining buyrug‘i o‘chirildi: {message.text}")
        except Exception as e:
            print(f"[ERROR] Buyruqni o‘chirishda xatolik: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()  # Token config.py dan olinadi
    
    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, admin_promoted))
    app.add_handler(MessageHandler(filters.REPLY, delete_messages))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, delete_user_commands))
    
    print("Bot ishga tushdi... Konsolni kuzating!")
    app.run_polling()

if __name__ == "__main__":
    main()
