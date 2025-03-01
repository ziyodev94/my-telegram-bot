from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN  # Tokenni config.py orqali olamiz
import asyncio

BOT_OWNER_ID = 7276556333  # <<< BU YERGA BOT EGASINING TELEGRAM ID sini qo‘ying

# /start komandasi uchun
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishga tushdi! /start buyrug'i qabul qilindi.")

# Bot admin qilinganda ishlaydigan funktsiya (faqat bot egasiga xabar yuboradi)
async def admin_promoted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = update.effective_chat.title
    chat_id = update.effective_chat.id

    message_text = (
        f"✅ Bot admin qilindi!\n"
        f"🏷 Guruh nomi: {chat_title}\n"
        f"🆔 Guruh ID: {chat_id}"
    )
    
    # Bot faqat egasiga xabar yuboradi
    await context.bot.send_message(chat_id=BOT_OWNER_ID, text=message_text)
    
    print(f"[LOGGING] Bot {chat_title} guruhida admin qilindi!")

# Xabarlarni o‘chirganda log qilish
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    # Faqat reply qilingan xabarlarni o'chiramiz
    if message.reply_to_message:
        try:
            await asyncio.sleep(5)  # 5 soniyadan keyin xabarni o‘chiramiz
            await message.delete()
            
            # Log xabarini bot egasiga yuborish
            log_message = (
                f"🗑 Xabar o‘chirildi!\n"
                f"👤 User: @{message.from_user.username if message.from_user.username else message.from_user.id}\n"
                f"🏷 Guruh: {message.chat.title}\n"
                f"📌 Xabar ID: {message.message_id}\n"
                f"✉️ Xabar: {message.text}"
            )
            await context.bot.send_message(chat_id=BOT_OWNER_ID, text=log_message)
            
            print(
                f"[DELETED] Xabar o'chirildi!\n"
                f"User: @{message.from_user.username if message.from_user.username else message.from_user.id}\n"
                f"Guruh: {message.chat.title}\n"
                f"Xabar ID: {message.message_id}\n"
                "--------------------------"
            )
        except Exception as e:
            print(f"[ERROR] Xabar o‘chirilmadi: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()  # Token config.py dan olinadi
    
    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, admin_promoted))
    app.add_handler(MessageHandler(filters.ALL, delete_messages))  # Faqat reply qilingan xabarlarni o‘chirish shart bilan ishlaydi
    
    print("Bot ishga tushdi... Konsolni kuzating!")
    app.run_polling()

if __name__ == "__main__":
    main()
