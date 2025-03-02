from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN
import asyncio

BOT_OWNER_ID = 7276556333
FORWARD_GROUP_ID = -2440778887

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishga tushdi! /start buyrug'i qabul qilindi.")

async def admin_promoted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = update.effective_chat.title
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=BOT_OWNER_ID, 
        text=f"✅ Bot admin qilindi!\n🏷 Guruh: {chat_title}\n🆔 ID: {chat_id}"
    )

async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        try:
            await asyncio.sleep(5)
            await update.message.delete()
            await context.bot.send_message(
                chat_id=BOT_OWNER_ID,
                text=f"🗑 {update.message.from_user.username}ning xabari o'chirildi!"
            )
        except Exception as e:
            print(f"Xatolik: {e}")

async def forward_channel_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    try:
        await context.bot.forward_message(
            chat_id=FORWARD_GROUP_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )
        await context.bot.send_message(
            chat_id=BOT_OWNER_ID,
            text=f"📢 {message.chat.title} kanalidan post jo'natildi!"
        )
    except Exception as e:
        print(f"Forward xatosi: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerni to'g'ri tartibda qo'shamiz
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, admin_promoted))
    app.add_handler(MessageHandler(
        filters.ChatType.CHANNEL & ~filters.COMMAND, 
        forward_channel_posts
    ))
    app.add_handler(MessageHandler(filters.ALL, delete_messages))
    
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
