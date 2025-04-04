import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, MessageHandler, CallbackQueryHandler, Filters, CallbackContext
import os

# توکن ربات
TOKEN = "7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo"

# آیدی عددی ادمین
ADMIN_ID = 5833077341

# لیست مکالمات در حال پاسخ
reply_targets = {}

# لاگ‌گیری
logging.basicConfig(level=logging.INFO)

# مدیریت دریافت پیام‌های کاربران (ناشناس)
def handle_messages(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.message

    if user.id == ADMIN_ID:
        return  # پیام‌های ادمین رو رد می‌کنیم

    # ساخت کیبورد شیشه‌ای پاسخ
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("پاسخ", callback_data=f"reply|{user.id}")]
    ])

    try:
        # بر اساس نوع پیام
        if msg.text:
            context.bot.send_message(chat_id=ADMIN_ID, text=msg.text, reply_markup=keyboard)
        elif msg.sticker:
            context.bot.send_sticker(chat_id=ADMIN_ID, sticker=msg.sticker.file_id, reply_markup=keyboard)
        elif msg.voice:
            context.bot.send_voice(chat_id=ADMIN_ID, voice=msg.voice.file_id, reply_markup=keyboard)
        elif msg.animation:
            context.bot.send_animation(chat_id=ADMIN_ID, animation=msg.animation.file_id, reply_markup=keyboard)
        elif msg.photo:
            photo = msg.photo[-1].file_id
            context.bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=msg.caption or "", reply_markup=keyboard)
        elif msg.video:
            context.bot.send_video(chat_id=ADMIN_ID, video=msg.video.file_id, caption=msg.caption or "", reply_markup=keyboard)
        elif msg.document:
            context.bot.send_document(chat_id=ADMIN_ID, document=msg.document.file_id, caption=msg.caption or "", reply_markup=keyboard)
    except Exception as e:
        print(f"خطا در ارسال پیام ناشناس به ادمین: {e}")

# وقتی ادمین روی "پاسخ" کلیک می‌کنه
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    data = query.data
    if data.startswith("reply|"):
        target_id = int(data.split("|")[1])
        reply_targets[ADMIN_ID] = target_id
        context.bot.send_message(chat_id=ADMIN_ID, text="خب، پیامت رو بفرست:")

# وقتی ادمین پیام ارسال می‌کنه
def handle_admin_reply(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return

    target_id = reply_targets.get(ADMIN_ID)
    if not target_id:
        return

    msg = update.message

    try:
        if msg.text:
            context.bot.send_message(chat_id=target_id, text=msg.text)
        elif msg.sticker:
            context.bot.send_sticker(chat_id=target_id, sticker=msg.sticker.file_id)
        elif msg.voice:
            context.bot.send_voice(chat_id=target_id, voice=msg.voice.file_id)
        elif msg.animation:
            context.bot.send_animation(chat_id=target_id, animation=msg.animation.file_id)
        elif msg.photo:
            context.bot.send_photo(chat_id=target_id, photo=msg.photo[-1].file_id, caption=msg.caption or "")
        elif msg.video:
            context.bot.send_video(chat_id=target_id, video=msg.video.file_id, caption=msg.caption or "")
        elif msg.document:
            context.bot.send_document(chat_id=target_id, document=msg.document.file_id, caption=msg.caption or "")
        
        reply_targets.pop(ADMIN_ID)
        context.bot.send_message(chat_id=ADMIN_ID, text="پیام ارسال شد.")
    except Exception as e:
        print(f"خطا در ارسال پاسخ: {e}")
        context.bot.send_message(chat_id=ADMIN_ID, text="خطا در ارسال پیام.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.user(user_id=ADMIN_ID) & Filters.all, handle_admin_reply))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, handle_messages))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
