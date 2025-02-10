from telegram import Update, ChatMember, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN  # Token config.py orqali olinadi

# /start komandasi uchun
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishga tushdi! /start buyrug'i qabul qilindi.")

# Buyruqlarni faqat adminlar ko‘ra oladigan qilish
async def hidden_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    
    member = await chat.get_member(user.id)
    
    if member.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        try:
            await update.message.delete()
            print(f"[HIDDEN COMMAND] {user.username} ({user.id}) bot buyruqlarini yubordi, lekin o‘chirildi.")
        except Exception as e:
            print(f"[ERROR] Buyruqni o‘chirishda xatolik: {e}")

# Bot admin qilinganda ishlaydigan funksiya
async def admin_promoted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = update.effective_chat.title
    await update.message.reply_text(
        f"✅ Bot ushbu guruhda admin qilindi!\n"
        f"🏷 Guruh nomi: {chat_title}\n"
        f"🆔 Guruh ID: {update.effective_chat.id}"
    )
    print(f"[LOGGING] Bot {chat_title} guruhida admin qilindi!")

# @Majbur_bot yuborgan spam, rasm, video, URL o‘chirish
async def delete_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message.forward_from and message.forward_from.username == "Majbur_bot":
        try:
            await message.delete()
            print(f"[SPAM DELETED] @{message.from_user.username} tomonidan yuborilgan reklama o‘chirildi.")
        except Exception as e:
            print(f"[ERROR] Spamni o‘chirishda muammo: {e}")

    elif message.photo or message.video or message.text and any(url in message.text for url in ["http", "www"]):
        try:
            await message.delete()
            print(f"[MEDIA/URL DELETED] @{message.from_user.username} tomonidan yuborilgan media yoki URL o‘chirildi.")
        except Exception as e:
            print(f"[ERROR] Media yoki URL o‘chirishda muammo: {e}")

# "Siz guruhga odam qo‘shishingiz kerak" xabarlarini saqlash
async def protect_important_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if "guruhga odam qo‘shishligiz kerak" in message.text and message.forward_from and message.forward_from.username == "Majbur_bot":
        print(f"[INFO] {message.from_user.username} botdan majburiy qo‘shish haqida xabar oldi, o‘chirilmadi.")
        return  # Xabarni saqlab qolamiz

    try:
        await message.delete()
        print(f"[MESSAGE DELETED] @{message.from_user.username} tomonidan yuborilgan xabar o‘chirildi.")
    except Exception as e:
        print(f"[ERROR] Oddiy foydalanuvchi xabarini o‘chirishda muammo: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()  # Token config.py dan olinadi
    
    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, admin_promoted))
    app.add_handler(MessageHandler(filters.COMMAND, hidden_commands))  # Buyruqlarni yashirish
    app.add_handler(MessageHandler(filters.ALL, delete_spam))  # Spam va media xabarlarni o‘chirish
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, protect_important_messages))  # Muhim xabarlarni saqlash

    print("Bot ishga tushdi... Konsolni kuzating!")
    app.run_polling()

if __name__ == "__main__":
    main()
