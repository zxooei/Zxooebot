import telebot
from telebot import types
import traceback

TOKEN = "7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo"
ADMIN_ID = 5833077341  # آیدی عددی تو

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "Hi")

@bot.message_handler(func=lambda message: True, content_types=[
    'text', 'sticker', 'animation', 'audio', 'voice', 'video', 'video_note', 'document'
])
def handle_user_message(message):
    if message.chat.id == ADMIN_ID:
        return

    try:
        # ارسال پیام به ادمین
        sent_msg = send_copy_to_admin(message)

        # دکمه پاسخ
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("پاسخ", callback_data=f"reply_{message.chat.id}")
        markup.add(btn)
        bot.send_message(ADMIN_ID, "می‌خوای جواب بدی؟", reply_markup=markup)

    except Exception:
        traceback.print_exc()
        bot.send_message(ADMIN_ID, "خطا هنگام کپی پیام!")

def send_copy_to_admin(message):
    if message.text:
        return bot.send_message(ADMIN_ID, message.text)
    elif message.sticker:
        return bot.send_sticker(ADMIN_ID, message.sticker.file_id)
    elif message.animation:
        return bot.send_animation(ADMIN_ID, message.animation.file_id)
    elif message.audio:
        return bot.send_audio(ADMIN_ID, message.audio.file_id)
    elif message.voice:
        return bot.send_voice(ADMIN_ID, message.voice.file_id)
    elif message.video:
        return bot.send_video(ADMIN_ID, message.video.file_id)
    elif message.video_note:
        return bot.send_video_note(ADMIN_ID, message.video_note.file_id)
    elif message.document:
        return bot.send_document(ADMIN_ID, message.document.file_id)
    else:
        return bot.send_message(ADMIN_ID, "این نوع پیام رو نمی‌تونم بفرستم.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def handle_reply_button(call):
    try:
        user_id = int(call.data.split("_")[1])
        bot.answer_callback_query(call.id)
        bot.send_message(ADMIN_ID, "منتظرم پیامتو بفرستی...")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_reply, user_id)

    except Exception:
        traceback.print_exc()
        bot.send_message(ADMIN_ID, "خطا در دکمه‌ی پاسخ")

def process_reply(message, user_id):
    try:
        if message.text:
            bot.send_message(user_id, message.text)
        elif message.sticker:
            bot.send_sticker(user_id, message.sticker.file_id)
        elif message.animation:
            bot.send_animation(user_id, message.animation.file_id)
        elif message.audio:
            bot.send_audio(user_id, message.audio.file_id)
        elif message.voice:
            bot.send_voice(user_id, message.voice.file_id)
        elif message.video:
            bot.send_video(user_id, message.video.file_id)
        elif message.video_note:
            bot.send_video_note(user_id, message.video_note.file_id)
        elif message.document:
            bot.send_document(user_id, message.document.file_id)
        else:
            bot.send_message(ADMIN_ID, "این نوع پیام رو نمی‌تونم بفرستم.")
    except Exception:
        traceback.print_exc()
        bot.send_message(ADMIN_ID, "خطا هنگام ارسال پیام!")

# اجرای دائمی ربات
while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        traceback.print_exc()
