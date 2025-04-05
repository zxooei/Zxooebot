import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
import sys

# تنظیمات ربات
TOKEN = '7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo'
ADMIN_ID = 5833077341  # آیدی عددی خودت رو بذار اینجا

bot = telebot.TeleBot(TOKEN)
user_message_map = {}

# اطلاع به ادمین وقتی ربات ری‌استارت میشه
def notify_admin():
    try:
        bot.send_message(ADMIN_ID, "ربات با موفقیت ری‌استارت شد.")
    except:
        pass

notify_admin()

# ساخت دکمه پاسخ
def make_reply_button(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("پاسخ بده", callback_data=f"reply_{user_id}"))
    return markup

# هندل همه نوع پیام
@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'sticker', 'animation', 'video_note', 'document'])
def handle_messages(message):
    if message.from_user.id == ADMIN_ID:
        return  # ادمین به خودش پیام نفرسته

    user_id = message.from_user.id
    user_message_map[str(message.message_id)] = user_id

    kwargs = {
        'chat_id': ADMIN_ID,
        'reply_markup': make_reply_button(user_id)
    }

    if message.content_type == 'text':
        bot.send_message(**kwargs, text=message.text)
    elif message.content_type == 'photo':
        bot.send_photo(**kwargs, photo=message.photo[-1].file_id, caption=message.caption or "")
    elif message.content_type == 'video':
        bot.send_video(**kwargs, video=message.video.file_id, caption=message.caption or "")
    elif message.content_type == 'voice':
        bot.send_voice(**kwargs, voice=message.voice.file_id)
    elif message.content_type == 'sticker':
        bot.send_sticker(**kwargs, sticker=message.sticker.file_id)
    elif message.content_type == 'animation':
        bot.send_animation(**kwargs, animation=message.animation.file_id, caption=message.caption or "")
    elif message.content_type == 'video_note':
        bot.send_video_note(**kwargs, data=message.video_note.file_id)
    elif message.content_type == 'document':
        bot.send_document(**kwargs, document=message.document.file_id, caption=message.caption or "")

    # تایید به کاربر
    bot.send_message(user_id, "پیام شما ارسال شد.")

# دکمه پاسخ
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def handle_reply(call):
    user_id = int(call.data.split("_")[1])
    msg = bot.send_message(ADMIN_ID, "پیامت رو برای این کاربر بفرست:")
    bot.register_next_step_handler(msg, forward_reply, user_id)
    bot.answer_callback_query(call.id, "منتظر پیامت هستم...")

def forward_reply(message, user_id):
    try:
        if message.content_type == 'text':
            bot.send_message(user_id, message.text)
        elif message.content_type == 'photo':
            bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption or "")
        elif message.content_type == 'video':
            bot.send_video(user_id, message.video.file_id, caption=message.caption or "")
        elif message.content_type == 'voice':
            bot.send_voice(user_id, message.voice.file_id)
        elif message.content_type == 'sticker':
            bot.send_sticker(user_id, message.sticker.file_id)
        elif message.content_type == 'animation':
            bot.send_animation(user_id, message.animation.file_id, caption=message.caption or "")
        elif message.content_type == 'video_note':
            bot.send_video_note(user_id, data=message.video_note.file_id)
        elif message.content_type == 'document':
            bot.send_document(user_id, message.document.file_id, caption=message.caption or "")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"خطا در ارسال پاسخ: {e}")

# ری‌استارت خودکار
def auto_restart():
    time.sleep(60)
    sys.exit()

threading.Thread(target=auto_restart).start()

# اجرای ربات
bot.infinity_polling()
