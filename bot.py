import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔹 تنظیمات اصلی
TOKEN = "7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo"
ADMIN_ID = 5833077341  # آیدی عددی شما

bot = telebot.TeleBot(TOKEN)

# 🔹 دیکشنری برای ذخیره کاربران و مسدودی‌ها
users = {}
blocked_users = set()

# 📌 شروع چت و خوشامدگویی
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "✅ سلام! اینجا می‌تونی پیام ناشناس ارسال کنی. \n\n✉️ هرچی دوست داری بفرست!")

# 📌 دریافت و ارسال پیام به ادمین با نمایش نام (و دکمه فقط در اولین پیام)
@bot.message_handler(func=lambda message: message.chat.id not in blocked_users, content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def forward_to_admin(message):
    user_id = message.chat.id
    username = message.from_user.first_name or "کاربر ناشناس"

    # 🔹 بررسی اینکه آیا این کاربر قبلاً پیام داده یا نه
    is_new_user = user_id not in users
    if is_new_user:
        users[user_id] = True
        bot.send_message(ADMIN_ID, f"🆕 پیام جدید از یک کاربر ناشناس دریافت شد!")

    # 🔹 نمایش نام کاربر فقط برای ادمین
    bot.send_message(ADMIN_ID, f"👤 نام فرستنده: {username} (@{message.from_user.username if message.from_user.username else 'ندارد'})\n🆔 آیدی: {user_id}")

    # 🔹 ایجاد دکمه فقط در اولین پیام کاربر
    keyboard = InlineKeyboardMarkup()
    if is_new_user:
        block_button = InlineKeyboardButton("🚫 بلاک کاربر", callback_data=f"block_{user_id}")
        keyboard.add(block_button)

    # 🔹 ارسال پیام کاربر ناشناس به ادمین
    if message.text:
        bot.send_message(ADMIN_ID, f"📩 پیام جدید:\n\n{message.text}", reply_markup=keyboard)
    elif message.photo:
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption="🖼 تصویر جدید دریافت شد.", reply_markup=keyboard)
    elif message.video:
        bot.send_video(ADMIN_ID, message.video.file_id, caption="🎥 ویدئوی جدید دریافت شد.", reply_markup=keyboard)
    elif message.document:
        bot.send_document(ADMIN_ID, message.document.file_id, caption="📄 فایل جدید دریافت شد.", reply_markup=keyboard)
    elif message.audio:
        bot.send_audio(ADMIN_ID, message.audio.file_id, caption="🎵 فایل صوتی جدید دریافت شد.", reply_markup=keyboard)
    elif message.voice:
        bot.send_voice(ADMIN_ID, message.voice.file_id, caption="🎤 ویس جدید دریافت شد.", reply_markup=keyboard)

# 📌 مدیریت کلیک روی دکمه‌های شیشه‌ای
@bot.callback_query_handler(func=lambda call: call.data.startswith("block_") or call.data.startswith("unblock_"))
def callback_handler(call):
    user_id = int(call.data.split("_")[1])

    if call.data.startswith("block_"):
        blocked_users.add(user_id)
        bot.send_message(ADMIN_ID, f"✅ کاربر {user_id} بلاک شد.")

        # 🔹 نمایش پیام و دکمه "✅ حذف مسدودیت" به ادمین
        keyboard = InlineKeyboardMarkup()
        unblock_button = InlineKeyboardButton("✅ حذف مسدودیت", callback_data=f"unblock_{user_id}")
        keyboard.add(unblock_button)
        bot.send_message(ADMIN_ID, f"🔴 کاربر {user_id} مسدود شد و دیگر نمی‌تواند پیام بفرستد.", reply_markup=keyboard)

        # 🔹 اطلاع‌رسانی به کاربر
        bot.send_message(user_id, "🚫 شما توسط ادمین مسدود شده‌اید و دیگر نمی‌توانید پیام ارسال کنید.")

    elif call.data.startswith("unblock_"):
        blocked_users.discard(user_id)
        bot.send_message(ADMIN_ID, f"✅ کاربر {user_id} از مسدودیت خارج شد.")
        bot.send_message(user_id, "✅ شما از مسدودیت خارج شدید و می‌توانید دوباره پیام ارسال کنید.")

# 📌 ارسال پاسخ ادمین به کاربر (ناشناس)
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    try:
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            bot.send_message(ADMIN_ID, "❌ فرمت اشتباه! لطفا این‌طور پاسخ بده:\n/reply [user_id] [پیام شما]")
            return

        user_id = int(parts[1])  # استخراج آیدی کاربر
        response_text = parts[2]  # استخراج پیام ادمین

        if user_id in blocked_users:
            bot.send_message(ADMIN_ID, "❌ این کاربر بلاک شده و نمی‌توان به او پیام ارسال کرد.")
            return

        bot.send_message(user_id, f"📩 پاسخ از ادمین:\n\n{response_text}")
        bot.send_message(ADMIN_ID, "✅ پیام شما ارسال شد!")
    
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ خطا در ارسال پاسخ: {str(e)}")

# 🔄 اجرای ربات
bot.polling()
