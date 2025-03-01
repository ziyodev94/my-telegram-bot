from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN  # Tokenni config.py orqali olamiz
import asyncio

# /start komandasi uchun
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishga tushdi! /start buyrug'i qabul qilindi.")

# Bot admin qilinganda ishlaydigan funktsiya (faqat botga xabar yuboradi)
async def admin_promoted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = update.effective_chat.title
    chat_id = update.effective_chat.id
    bot_owner_id = context.bot.bot_id  # Bot egasining ID sini olish

    message_text = (
        f"✅ Bot admin qilindi!\n"
        f"🏷 Guruh nomi: {chat_title}\n"
        f"🆔 Guruh ID: {chat_id}"
    )
    
    # Bot faqat o'ziga xabar yuboradi
    await context.bot.send_message(chat_id=bot_owner_id, text=message_text)
    
    print(f"[LOGGING] Bot {chat_title} guruhida admin qilindi!")

# Xabarlarni o‘chirganda log qilish
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    bot_owner_id = context.bot.bot_id  # Bot egasining ID sini olish
    
    # Faqat reply qilingan xabarlarni o'chiramiz
    if message.reply_to_message:
        try:
            await asyncio.sleep(5)  # 5 soniyadan keyin xabarni o‘chiramiz
            await message.delete()
            
            # Log xabarini bot egasiga yuborish
            log_message = (
                f"🗑 Xabar o‘chirildi!\n"
                f"👤 User: @{message.from_user.username}\n"
                f"🏷 Guruh: {message.chat.title}\n"
                f"📌 Xabar ID: {message.message_id}\n"
                f"✉️ Xabar: {message.text}"
            )
            await context.bot.send_message(chat_id=bot_owner_id, text=log_message)
            
            print(
                f"[DELETED] Xabar o'chirildi!\n"
                f"User: @{message.from_user.username}\n"
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
    app.add_handler(MessageHandler(filters.REPLY, delete_messages))
    
    print("Bot ishga tushdi... Konsolni kuzating!")
    app.run_polling()

if __name__ == "__main__":
    main()
