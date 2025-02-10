from telegram import Update, MessageEntity
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN  # Token config.py dan olinadi

# Foydalanuvchilar yozgan va guruhda chiqib qoladigan buyruqlarni o‘chirish uchun so‘zlar
DELETE_KEYWORDS = [
    "/start@Majbur_bot",
    "/guruh",
    "/guruh_off",
    "/kanal",
    "/kanal_off",
    "/bal",
    "/meni",
    "/sizni",
    "/top",
    "/nol",
    "/del"
]

# @Majbur_bot dan keladigan aniq reklama xabarlari
DELETE_MESSAGES = [
    "📣KANAL va 👥GURUHGA  - ISTAGANCHA ODAM YIG'ISHDA YORDAM BERADIGAN BOT !",
    "👥GURUHGA ISTAGANCHA ODAM YIGISH",
    "1) 📣 KANALGA ODAM YIGʻISH - Man guruhingizdagi a'zolarni kanalga a'zo bo'lmaguncha yozdirmayman ❗️",
    "2) 👥 GURUHGA ODAM YIGʻISH - Man guruhingizdagi odamlar guruhga odam qoʻshishmasa yozdirmayman ❗️",
    "3) 📊 GURUH A'ZOLARINI SANAYDI - guruhga kim qancha odam qoʻshgan va eng kop odam qoʻshganlarni aniqlayman❗️",
    "👉 /help   -  🔖 TEKSLI QO'LLANMA",
    "👨🏻‍✈️ Bot ushbu vazifalarni bajarish uchun guruhingizda toʻliq ADMIN bulishi shart !"
]

# @Majbur_bot tomonidan yuborilgan xabarlarni aniqlash uchun bot username'i
TARGET_BOT_USERNAME = "Majbur_bot"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /start komandasi """
    await update.message.reply_text("🤖 Bot ishga tushdi janob! /start buyrug'i qabul qilindi.")


async def delete_unwanted_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Foydalanuvchilar botga tegishli buyruqlarni yoki Majbur_bot reklama xabarlarini yozsa, ularni o‘chiradi. """
    message = update.message

    # 1. Agar foydalanuvchi DELETE_KEYWORDS ro‘yxatidagi so‘zlardan birini yozsa, o‘chiramiz
    if message.text and any(keyword in message.text for keyword in DELETE_KEYWORDS):
        await message.delete()
        print(f"[DELETED] Foydalanuvchi yozgan botga tegishli buyruq o‘chirildi: {message.text}")
        return

    # 2. Agar xabar @Majbur_bot tomonidan yuborilgan bo‘lsa
    if message.from_user and message.from_user.username == TARGET_BOT_USERNAME:
        # Majbur_bot dan kelgan aniq reklama matnlarini o‘chirib tashlash
        for msg in DELETE_MESSAGES:
            if msg in message.text:
                await message.delete()
                print(f"[DELETED] @Majbur_bot reklama xabari o‘chirildi: {message.message_id}")
                return

        # 3. Agar xabarda URL, rasm, video bo‘lsa, uni ham o‘chirib tashlash
        if (
            message.entities
            and any(entity.type in ["url", "text_link"] for entity in message.entities)
        ) or message.photo or message.video:
            await message.delete()
            print(f"[DELETED] @Majbur_bot tomonidan yuborilgan media yoki URL xabari o‘chirildi: {message.message_id}")
            return


def main():
    """ Botni ishga tushirish """
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, delete_unwanted_messages))

    print("Bot ishga tushdi... Konsolni kuzating!")
    app.run_polling()


if __name__ == "__main__":
    main()




