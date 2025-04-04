from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import logging
import threading
import time

# تنظیمات ربات
TOKEN = '7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo'
ADMIN_ID = 5833077341  # عددی و بدون کوتیشن
SPECIAL_ID = 7248220184  # آیدی خاصی که باید هر ۲ دقیقه پیام بگیره

# لاگ‌ها برای بررسی خطا
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# پیام شروع
def start(update: Update, context: CallbackContext):
    update.message.reply_text("پیامتو بفرست تا برسه دستم!")

# ارسال دکمه پاسخ فقط برای ادمین
def send_to_admin_with_button(bot, message, user_id):
    user_name = message.from_user.full_name
    user_username = message.from_user.username
    user_id = message.from_user.id
    
    # نمایش اسم و آیدی کاربر به ادمین
    forward = bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat_id, message_id=message.message_id)
    
    keyboard = [
        [InlineKeyboardButton("پاسخ به این پیام", callback_data=f"reply|{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # پیام ادمین با اطلاعات ارسال کننده
    bot.send_message(chat_id=ADMIN_ID, text=f"پیامی از {user_name} (@{user_username}) رسید.\n\nID: {user_id}\n\nبا کلیک روی دکمه زیر می‌تونی بهش پاسخ بدی.", reply_markup=reply_markup)

# هندل همه‌ی نوع پیام
def handle_all_messages(update: Update, context: CallbackContext):
    message = update.message
    user_id = message.from_user.id
    send_to_admin_with_button(context.bot, message, user_id)
    message.reply_text("پیامت رسید! اگه لازم باشه جواب می‌دم.")

# گرفتن ورودی ادمین برای پاسخ
def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data.startswith("reply|"):
        target_user_id = int(data.split("|")[1])
        context.user_data["reply_to"] = target_user_id
        context.bot.send_message(chat_id=ADMIN_ID, text="خب! جوابتو تایپ کن تا براش بفرستم.")

# وقتی ادمین پیام می‌فرسته به کاربر
def admin_reply(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        return
    target = context.user_data.get("reply_to")
    if target:
        context.bot.send_message(chat_id=target, text=f"یه پیام از ادمین برات اومده:\n\n{update.message.text}")
        update.message.reply_text("فرستادم براش!")
        context.user_data["reply_to"] = None
    else:
        update.message.reply_text("اول باید رو دکمه‌ی «پاسخ به این پیام» بزنی!")

# ارسال نقطه هر ۲ دقیقه به SPECIAL_ID
def keep_bot_alive():
    while True:
        try:
            bot.send_message(chat_id=SPECIAL_ID, text=".")
        except Exception as e:
            logger.error(f"خطا در keep_alive: {e}")
        time.sleep(120)

# اجرای ربات
def main():
    global bot
    updater = Updater(TOKEN, use_context=True)
    bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_callback))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, handle_all_messages))
    dp.add_handler(MessageHandler(Filters.text & Filters.chat(chat_id=ADMIN_ID), admin_reply))

    # اجرای ترد جدا برای زنده نگه داشتن ربات
    threading.Thread(target=keep_bot_alive, daemon=True).start()

    updater.start_polling()
    print("ربات روشنه...")
    updater.idle()

if __name__ == '__main__':
    main()
