import telebot
import os
from flask import Flask, request

TOKEN = '7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo'
ADMIN_ID = 5833077341  # آیدی عددی ادمین

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

blocked_users = set()
users = {}

@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document'])
def handle_message(message):
    chat_id = message.chat.id
    if chat_id in blocked_users:
        return

    users[chat_id] = message.from_user.first_name
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🚫 بلاک", callback_data=f"block_{chat_id}"))

    if message.text:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید از {users[chat_id]}:\n\n{message.text}", reply_markup=markup)
    elif message.photo:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید از {users[chat_id]}:")
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, reply_markup=markup)
    elif message.video:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید از {users[chat_id]}:")
        bot.send_video(ADMIN_ID, message.video.file_id, reply_markup=markup)
    elif message.voice:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید از {users[chat_id]}:")
        bot.send_voice(ADMIN_ID, message.voice.file_id, reply_markup=markup)
    elif message.document:
        bot.send_message(ADMIN_ID, f"📩 فایل جدید از {users[chat_id]}:")
        bot.send_document(ADMIN_ID, message.document.file_id, reply_markup=markup)

    bot.send_message(chat_id, "✅ پیامت ارسال شد.")

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def reply_to_user(message):
    if "📩 پیام جدید از" in message.reply_to_message.text:
        user_id = int(message.reply_to_message.text.split("📩 پیام جدید از ")[1].split(":")[0])
        if user_id in blocked_users:
            bot.send_message(ADMIN_ID, "⛔ این کاربر بلاک شده است.")
        else:
            bot.send_message(user_id, message.text)
            bot.send_message(ADMIN_ID, "✅ پیام ارسال شد.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = int(call.data.split("_")[1])
    if call.data.startswith("block_"):
        blocked_users.add(chat_id)
        bot.send_message(ADMIN_ID, f"🚫 کاربر {users[chat_id]} بلاک شد.")
        bot.send_message(chat_id, "⛔ شما از ربات مسدود شدید.")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🔓 آنبلاک", callback_data=f"unblock_{chat_id}"))
        bot.send_message(ADMIN_ID, "⬇ برای آنبلاک دکمه زیر را بزن:", reply_markup=markup)
    elif call.data.startswith("unblock_"):
        blocked_users.discard(chat_id)
        bot.send_message(ADMIN_ID, f"✅ کاربر {users[chat_id]} آنبلاک شد.")

@server.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def index():
    return "ربات روشن است"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://نام_سرویس_در_Render.onrender.com/{TOKEN}")
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
