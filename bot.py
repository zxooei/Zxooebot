
‏from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
‏from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

‏TOKEN = '7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo'  # توکن رباتت رو اینجا بذار
‏ADMIN_ID = 5833077341  # آی‌دی عددی خودت اینجا جایگزین کن

‏pending_replies = {}

‏def start(update: Update, context: CallbackContext):
‏    update.message.reply_text("سلام پیامتو برام بفرست!")

‏def send_to_admin(update: Update, context: CallbackContext):
‏    user = update.effective_user
‏    user_id = user.id
‏    username = user.username or "کاربر"
‏    caption = f"پیام از {username} (ID: {user_id})"

‏    keyboard = InlineKeyboardMarkup([
‏        [InlineKeyboardButton("جواب بده", callback_data=f"reply_{user_id}")]
    ])

‏    msg = update.message

‏    if msg.text:
‏        context.bot.send_message(chat_id=ADMIN_ID, text=f"{caption}:\n{msg.text}", reply_markup=keyboard)
‏    elif msg.voice:
‏        context.bot.send_voice(chat_id=ADMIN_ID, voice=msg.voice.file_id, caption=caption, reply_markup=keyboard)
‏    elif msg.sticker:
‏        context.bot.send_sticker(chat_id=ADMIN_ID, sticker=msg.sticker.file_id)
‏        context.bot.send_message(chat_id=ADMIN_ID, text=caption, reply_markup=keyboard)
‏    elif msg.animation:
‏        context.bot.send_animation(chat_id=ADMIN_ID, animation=msg.animation.file_id, caption=caption, reply_markup=keyboard)
‏    elif msg.photo:
‏        largest_photo = msg.photo[-1]
‏        context.bot.send_photo(chat_id=ADMIN_ID, photo=largest_photo.file_id, caption=caption, reply_markup=keyboard)
‏    elif msg.video:
‏        context.bot.send_video(chat_id=ADMIN_ID, video=msg.video.file_id, caption=caption, reply_markup=keyboard)
‏    else:
‏        msg.reply_text("اوه! این نوع پیام رو فعلاً نمی‌تونم بفرستم.")
‏        return

‏    msg.reply_text("دمت گرم! پیامت رسید و ناشناس فرستاده شد.")

‏def handle_user_messages(update: Update, context: CallbackContext):
‏    if update.effective_user.id != ADMIN_ID:
‏        send_to_admin(update, context)

‏def handle_callback(update: Update, context: CallbackContext):
‏    query = update.callback_query
‏    query.answer()

‏    if query.from_user.id != ADMIN_ID:
‏        query.edit_message_text("این دکمه فقط برای مدیر فعاله.")
‏        return

‏    data = query.data
‏    if data.startswith("reply_"):
‏        target_id = int(data.split("_")[1])
‏        pending_replies[ADMIN_ID] = target_id
‏        query.edit_message_text("خب حالا جوابشو بفرست")

‏def handle_admin_response(update: Update, context: CallbackContext):
‏    if update.effective_user.id != ADMIN_ID:
‏        return

‏    if ADMIN_ID not in pending_replies:
‏        update.message.reply_text("هیچ کسی رو برای جواب دادن انتخاب نکردی.")
‏        return

‏    target_id = pending_replies.pop(ADMIN_ID)
‏    msg = update.message

‏    try:
‏        if msg.text:
‏            context.bot.send_message(chat_id=target_id, text=msg.text)
‏        elif msg.voice:
‏            context.bot.send_voice(chat_id=target_id, voice=msg.voice.file_id)
‏        elif msg.sticker:
‏            context.bot.send_sticker(chat_id=target_id, sticker=msg.sticker.file_id)
‏        elif msg.animation:
‏            context.bot.send_animation(chat_id=target_id, animation=msg.animation.file_id)
‏        elif msg.photo:
‏            largest_photo = msg.photo[-1]
‏            context.bot.send_photo(chat_id=target_id, photo=largest_photo.file_id)
‏        elif msg.video:
‏            context.bot.send_video(chat_id=target_id, video=msg.video.file_id)
‏        else:
‏            msg.reply_text("اوه! این نوع پیام رو نمی‌تونم بفرستم.")
‏            return

‏        msg.reply_text("اوکی، جواب فرستاده شد.")

‏    except Exception as e:
‏        msg.reply_text(f"یه مشکلی خوردیم: {e}")

‏def main():
‏    updater = Updater(TOKEN, use_context=True)
‏    dp = updater.dispatcher

‏    dp.add_handler(CommandHandler('start', start))
‏    dp.add_handler(CallbackQueryHandler(handle_callback))
‏    dp.add_handler(MessageHandler(Filters.user(user_id=ADMIN_ID), handle_admin_response))

‏    dp.add_handler(MessageHandler(
‏        Filters.private & (
‏            Filters.text | Filters.voice | Filters.sticker |
‏            Filters.animation | Filters.photo | Filters.video
‏        ) & ~Filters.user(user_id=ADMIN_ID),
‏        handle_user_messages
    ))

‏    updater.start_polling()
‏    updater.idle()

‏if __name__ == '__main__':
‏    main()
