import telebot
from telebot import types

# توکن ربات خود را اینجا وارد کنید
TOKEN = "7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo"

# ایدی مدیر ربات (شما)
ADMIN_ID = 5833077341  # ایدی عددی خودتون رو اینجا وارد کنید!

# ساخت ربات
bot = telebot.TeleBot(TOKEN)

# پیام خوشامد
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "با من ناشناس حرف بزن")

# تابع برای فوروارد کردن پیام و دکمه شیشه‌ای برای پاسخ دادن
@bot.message_handler(func=lambda message: message.text != "/start")  # جلوگیری از ارسال /start
def forward_message(message):
    user = message.from_user
    text = message.text if message.text else "این پیام متنی نبود! 🤔"
    
    # فوروارد کردن پیام به شما به صورت فوروارد تلگرامی
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    
    # ارسال پیام جدید به شما با دکمه برای پاسخ دادن
    if message.chat.id != ADMIN_ID:  # فقط برای شما دکمه نمایش داده میشه
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("می‌خوای جواب بدی؟ ✉️", callback_data=f"reply_{message.message_id}")
        markup.add(button)
        
        # ارسال پیام همراه با دکمه به شما
        bot.send_message(ADMIN_ID, "این پیام رو دریافت کردم. می‌خوای جواب بدی؟", reply_markup=markup)

# تابع برای ارسال پاسخ به پیام
@bot.callback_query_handler(func=lambda call: True)
def reply_to_message(call):
    message_id = int(call.data.split("_")[1])  # استخراج message_id برای ریپلای

    # منتظر دریافت پیام از شما (مدیر)
    bot.answer_callback_query(call.id, "حالا هر پیامی که می‌خوای بفرست، من آماده‌ام! ✨")
    
    # ذخیره message_id برای ارسال جواب
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, send_reply, message_id)

# تابع برای ارسال پاسخ به پیام مورد نظر
def send_reply(message, message_id):
    user = message.from_user

    # ارسال پاسخ به کاربر با ریپلای روی پیام
    if message.text:
        bot.send_message(user.id, message.text, reply_to_message_id=message_id)
    elif message.sticker:
        bot.send_sticker(user.id, message.sticker.file_id, reply_to_message_id=message_id)
    elif message.animation:
        bot.send_animation(user.id, message.animation.file_id, reply_to_message_id=message_id)
    elif message.audio:
        bot.send_audio(user.id, message.audio.file_id, reply_to_message_id=message_id)
    elif message.video:
        bot.send_video(user.id, message.video.file_id, reply_to_message_id=message_id)

# اجرای ربات
bot.polling(none_stop=True)
