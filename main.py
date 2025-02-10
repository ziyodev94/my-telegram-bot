from telegram import Update, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN  # Token config.py dan olinadi

# ❌ Oddiy foydalanuvchilar / bilan boshlanuvchi barcha buyruqlarni avtomatik o‘chirish
async def delete_user_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Agar oddiy foydalanuvchi /buyruq bossa, xabarni o‘chiradi """
    message = update.message

    if not message:
        return
    
    user_id = message.from_user.id
    chat = update.effective_chat
    chat_member = await chat.get_member(user_id)

    if chat_member.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if message.text and message.text.startswith("/"):
            await message.delete()
            print(f"[DELETED] Foydalanuvchi {message.from_user.username} buyruq bosdi va o‘chirildi: {message.text}")
            return

# ❌ @Majbur_bot reklama xabarlarini va spamni o‘chirish
DELETE_MESSAGES = [
    "📣KANAL va 👥GURUHGA  - ISTAGANCHA ODAM YIG'ISHDA YORDAM BERADIGAN BOT !",
    "👥GURUHGA ISTAGANCHA ODAM YIGISH",
    "1) 📣 KANALGA ODAM YIGʻISH - Man guruhingizdagi a'zolarni kanalga a'zo bo'lmaguncha yozdirmayman ❗️",
    "2) 👥 GURUHGA ODAM YIGʻISH - Man guruhingizdagi odamlar guruhga odam qoʻshishmasa yozdirmayman ❗️",
    "3) 📊 GURUH A'ZOLARINI SANAYDI - guruhga kim qancha odam qoʻshgan va eng kop odam qoʻshganlarni aniqlayman❗️",
    "👉 /help   -  🔖 TEKSLI QO'LLANMA",
    "👨🏻‍✈️ Bot ushbu vazifalarni bajarish uchun guruhingizda toʻliq ADMIN bulishi shart !"
]

TARGET_BOT_USERNAME = "Majbur_bot"

async def delete_majburbot_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Agar @Majbur_bot dan reklama yoki spam kelib qolsa, o‘chiradi """
    message = update.message

    if message.from_user and message.from_user.username == TARGET_BOT_USERNAME:
        for msg in DELETE_MESSAGES:
            if msg in message.text:
                await message.delete()
                print(f"[DELETED] @Majbur_bot reklama xabari o‘chirildi: {message.message_id}")
                return
        
        if message.entities or message.photo or message.video:
            await message.delete()
            print(f"[DELETED] @Majbur_bot media yoki link xabari o‘chirildi: {message.message_id}")
            return

# ❌ Guruhdagi kanal nomidan kelgan xabarlarga reply qilingan xabarlarni o‘chirish
async def delete_replies_to_channel_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Agar kimdir kanal nomidan kelgan xabarga reply bersa, reply qilingan xabar o‘chiriladi """
    message = update.message

    if message and message.reply_to_message:
        replied_message = message.reply_to_message

        if replied_message.sender_chat and replied_message.sender_chat.type == "channel":
            await message.delete()
            print(f"[DELETED] Kanal nomidan kelgan xabarga reply qilgan xabar o‘chirildi: {message.message_id}")
            return

# 🔒 Bot buyruqlari faqat adminlarga ko‘rinishi uchun
async def set_admin_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Botning buyruqlari faqat adminlarga ko‘rinadigan bo‘ladi """
    chat = update.effective_chat
    bot = context.bot
    commands = [
        ("start", "Botni ishga tushirish"),
        ("help", "Yordam"),
        ("settings", "Sozlamalar"),
    ]

    await bot.set_my_commands(commands, scope={"type": "chat_administrators", "chat_id": chat.id})
    print(f"[UPDATED] Buyruqlar faqat adminlarga ko‘rinadigan qilindi!")

# 🔄 Botni ishga tushirish
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", set_admin_commands))
    app.add_handler(MessageHandler(filters.ALL, delete_user_commands))
    app.add_handler(MessageHandler(filters.ALL, delete_majburbot_messages))
    app.add_handler(MessageHandler(filters.ALL, delete_replies_to_channel_messages))

    print("Bot ishga tushdi... Konsolni kuzating!")
    app.run_polling()

if __name__ == "__main__":
    main()




