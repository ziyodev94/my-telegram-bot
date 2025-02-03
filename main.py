from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7931935861:AAHhCRQKa60V2xBEqm2atQCl21NKLLP-RKU"

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
    print(f"[LOGGING] Bot {chat_title} guruhida admin qilindi!")

# Xabarlarni o'chirganda log qilish
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
            print(f"[ERROR] Xabar o'chirilmadi: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, admin_promoted))
    app.add_handler(MessageHandler(filters.REPLY, delete_messages))
    
    print("Bot ishga tushdi... Konsolni kuzating!")
    app.run_polling()

if __name__ == "__main__":
    main()
