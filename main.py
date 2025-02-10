from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN  # Token config.py dan olinadi

# /start komandasi
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
    print(f"[LOGGING] Bot {chat_title} guruhida admin qilindi!")

# Reply qilingan xabarlarni o‘chirish
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Log chiqarish - bot boshqa guruhlarda ishlayotganini tekshirish uchun
    print(f"[LOG] Xabar qabul qilindi - Guruh: {message.chat.title}, ID: {message.chat.id}")

    if message and message.reply_to_message:  # Agar reply bo‘lsa
        try:
            await message.reply_to_message.delete()  # Reply qilingan xabarni o‘chirish
            print(f"[DELETED] Reply qilingan xabar o‘chirildi: {message.reply_to_message.message_id}")
        except Exception as e:
            print(f"[ERROR] Reply qilingan xabar o‘chirilmadi: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()  # Token config.py dan olinadi
    
    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ChatMemberUpdated.MY_CHAT_MEMBER, admin_promoted))
    app.add_handler(MessageHandler(filters.ALL, delete_messages))
    
    print("Bot ishga tushdi... Konsolni kuzating janob!")
    app.run_polling()

if __name__ == "__main__":
    main()


