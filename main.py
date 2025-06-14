from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN
import asyncio

BOT_OWNER_ID = 7276556333
FORWARD_GROUP_ID = -1002284823280

# Kanal post ID ↔ Guruh post ID mapping
message_map = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("https://telegram.me/joinchat/Gz9BpoyJmkgwOGM6")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start – Botni ishga tushuradi\n"
        "/help – Yordam\n"
        "Kanal postlari guruhga ko‘chiriladi\n"
        "Matn va caption tahriri: bevosita yangilanadi\n"
        "Media o‘zgarsa: guruhdagi post o‘chib, qayta yuboriladi"
    )

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

# Yangi kanal postni guruhga copy qilib yuborish
async def handle_new_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post
    try:
        copied = await message.copy(chat_id=FORWARD_GROUP_ID)
        message_map[message.message_id] = copied.message_id
        await context.bot.send_message(
            chat_id=BOT_OWNER_ID,
            text=f"📥 Yangi post ko‘chirildi: {message.chat.title or 'Nomaʼlum kanal'}"
        )
    except Exception as e:
        print(f"Yangi post xatolik: {e}")

# Tahrir bo‘lsa — matn/caption edit qilinadi, media bo‘lsa qayta tashlanadi
async def handle_edited_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.edited_channel_post
    try:
        original_id = message.message_id
        if original_id in message_map:
            target_id = message_map[original_id]

            # 1. Faqat matnli post bo‘lsa
            if message.text:
                try:
                    await context.bot.edit_message_text(
                        chat_id=FORWARD_GROUP_ID,
                        message_id=target_id,
                        text=message.text
                    )
                    return
                except Exception as e:
                    if "Message is not modified" in str(e):
                        print("⚠️ Matn o‘zgarmagan")
                    else:
                        print("❌ Matn tahriri xatolik:", e)

            # 2. Caption tahriri (media o‘zgarmagan bo‘lsa)
            elif message.caption and not message.media_group_id:
                try:
                    await context.bot.edit_message_caption(
                        chat_id=FORWARD_GROUP_ID,
                        message_id=target_id,
                        caption=message.caption
                    )
                    return
                except Exception as e:
                    if "Message is not modified" in str(e):
                        print("⚠️ Caption o‘zgarmagan")
                    else:
                        print("❌ Caption tahriri xatolik:", e)

            # 3. Media o‘zgargan bo‘lsa — eski postni o‘chiramiz, yangisini yuboramiz
            await context.bot.delete_message(
                chat_id=FORWARD_GROUP_ID,
                message_id=target_id
            )
            new_msg = await message.copy(chat_id=FORWARD_GROUP_ID)
            message_map[original_id] = new_msg.message_id
            await context.bot.send_message(
                chat_id=BOT_OWNER_ID,
                text=f"🔁 Media yangilandi – post qayta yuborildi: {message.chat.title or 'Kanal'}"
            )
        else:
            print("⚠️ Tahrir qilingan post mappingda topilmadi")
    except Exception as e:
        print(f"❌ Umumiy tahrir xatolik: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, admin_promoted))

    # Yangi kanal postlar
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, handle_new_channel_post))

    # Tahrirlangan kanal postlar
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_CHANNEL_POST, handle_edited_channel_post))

    # Reply xabarlar uchun 5s o‘chirish
    app.add_handler(MessageHandler(filters.ALL, delete_messages))

    print("✅ Bot main.py bilan ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
