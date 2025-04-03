import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔹 تنظیمات اصلی
TOKEN = "7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo"
ADMIN_ID = 5833077341  # آیدی عددی شما

bot = telebot.TeleBot(TOKEN)

# لیست کاربران بلاک‌شده
blocked_users = set()

# دیکشنری برای ذخیره اطلاعات کاربران
users = {}

# ==== هندلر دریافت پیام ====
@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document'])
def handle_message(message):
    chat_id = message.chat.id

    # اگر کاربر بلاک شده باشد، پیامش پردازش نمی‌شود
    if chat_id in blocked_users:
        return

    # ذخیره نام فرستنده
    users[chat_id] = message.from_user.first_name

    # ایجاد دکمه‌ی بلاک برای پیام اول
    markup = InlineKeyboardMarkup()
    btn_block = InlineKeyboardButton("🚫 بلاک", callback_data=f"block_{chat_id}")
    markup.add(btn_block)

    # ارسال پیام متنی
    if message.text:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید از {users[chat_id]}:\n\n{message.text}", reply_markup=markup)

    # ارسال عکس
    elif message.photo:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید از {users[chat_id]}:")
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, reply_markup=markup)

    # ارسال ویدیو
    elif message.video:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید از {users[chat_id]}:")
        bot.send_video(ADMIN_ID, message.video.file_id, reply_markup=markup)

    # ارسال ویس
    elif message.voice:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید از {users[chat_id]}:")
        bot.send_voice(ADMIN_ID, message.voice.file_id, reply_markup=markup)

    # ارسال فایل
    elif message.document:
        bot.send_message(ADMIN_ID, f"📩 فایل جدید از {users[chat_id]}:")
        bot.send_document(ADMIN_ID, message.document.file_id, reply_markup=markup)

    # ارسال پیام تایید برای کاربر
    bot.send_message(chat_id, "✅ پیامت ارسال شد.")

# ==== ارسال پاسخ از ادمین به کاربر ====
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def reply_to_user(message):
    if message.reply_to_message and "📩 پیام جدید از" in message.reply_to_message.text:
        user_id = int(message.reply_to_message.text.split("📩 پیام جدید از ")[1].split(":")[0])
        if user_id in blocked_users:
            bot.send_message(ADMIN_ID, "⛔ این کاربر بلاک شده است و نمی‌توان به او پیام داد.")
        else:
            bot.send_message(user_id, message.text)
            bot.send_message(ADMIN_ID, "✅ پیام ارسال شد.")

# ==== بلاک و آنبلاک کاربران ====
@bot.callback_query_handler(func=lambda call: call.data.startswith("block_") or call.data.startswith("unblock_"))
def handle_block_unblock(call):
    chat_id = int(call.data.split("_")[1])

    if call.data.startswith("block_"):
        blocked_users.add(chat_id)
        bot.send_message(ADMIN_ID, f"🚫 کاربر {users[chat_id]} بلاک شد.")
        bot.send_message(chat_id, "⛔ شما از ربات مسدود شدید.")
        
        # دکمه‌ی آنبلاک اضافه شود
        markup = InlineKeyboardMarkup()
        btn_unblock = InlineKeyboardButton("🔓 آنبلاک", callback_data=f"unblock_{chat_id}")
        bot.send_message(ADMIN_ID, f"🔒 برای رفع مسدودیت این کاربر دکمه‌ی زیر را بزنید:", reply_markup=markup)

    elif call.data.startswith("unblock_"):
        blocked_users.discard(chat_id)
        bot.send_message(ADMIN_ID, f"✅ کاربر {users[chat_id]} آنبلاک شد.")

bot.polling()
