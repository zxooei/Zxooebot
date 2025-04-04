import telebot
from telebot import types
import traceback

# توکن و آیدی عددی خودت رو اینجا بذار
TOKEN = "7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo"
ADMIN_ID = 5833077341  # آیدی عددی خودت

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "با من ناشناس حرف بزن")

@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker', 'animation', 'audio', 'voice', 'video', 'video_note', 'document'])
def handle_user_message(message):
    if message.chat.id == ADMIN_ID:
        return

    try:
        # ارسال محتوای پیام کاربر برای ادمین (تو)
        sent_msg = send_anonymous_copy_to_admin(message)

        # ساخت دکمه فقط برای ادمین
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("پاسخ", callback_data=f"reply_{message.chat.id}_{sent_msg.message_id}")
        markup.add(btn)

        bot.send_message(ADMIN_ID, "می‌خوای جواب بدی؟", reply_markup=markup)

    except Exception:
        traceback.print_exc()
        bot.send_message(ADMIN_ID, "یه مشکلی پیش اومد موقع کپی پیام!")

def send_anonymous_copy_to_admin(message):
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
        data = call.data.split("_")
        target_id = int(data[1])
        reply_to_msg_id = int(data[2])

        bot.answer_callback_query(call.id)
        bot.send_message(ADMIN_ID, "منتظرم پیامتو بفرستی...")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_reply, target_id, reply_to_msg_id)

    except Exception:
        traceback.print_exc()
        bot.send_message(ADMIN_ID, "خطا توی دکمه‌ی پاسخ")

def process_reply(message, target_id, reply_to_msg_id):
    try:
        kwargs = {'chat_id': target_id, 'reply_to_message_id': reply_to_msg_id}

        if message.text:
            bot.send_message(**kwargs, text=message.text)
        elif message.sticker:
            bot.send_sticker(**kwargs, sticker=message.sticker.file_id)
        elif message.animation:
            bot.send_animation(**kwargs, animation=message.animation.file_id)
        elif message.audio:
            bot.send_audio(**kwargs, audio=message.audio.file_id)
        elif message.voice:
            bot.send_voice(**kwargs, voice=message.voice.file_id)
        elif message.video:
            bot.send_video(**kwargs, video=message.video.file_id)
        elif message.video_note:
            bot.send_video_note(**kwargs, video_note=message.video_note.file_id)
        elif message.document:
            bot.send_document(**kwargs, document=message.document.file_id)
        else:
            bot.send_message(ADMIN_ID, "این نوع پیام رو نمی‌تونم بفرستم.")
    except Exception:
        traceback.print_exc()
        bot.send_message(ADMIN_ID, "خطا موقع فرستادن جواب!")

# جلوگیری از کرش ربات
while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        traceback.print_exc()
        print("ربات کرش کرد، دوباره راه‌اندازی می‌شه...")
