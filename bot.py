from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import time
import threading

# توکن ربات و ایدی‌ها
TOKEN = '7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo'  # جایگزین کن با توکن رباتت
ADMIN_ID = '5833077341'  # ایدی ادمین
SPECIAL_ID = '7248220184'  # ایدی خاص که هر ۲ دقیقه نقطه می‌فرسته

# تنظیمات لاگ برای ثبت خطاها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# این تابع برای شروع ارتباط با ربات استفاده می‌شود
def start(update: Update, context):
    update.message.reply_text('سلام! پیامتو بفرست.☁️')

# این تابع برای مدیریت پیام‌های متنی استفاده می‌شود
def handle_message(update: Update, context):
    # ارسال پیام دریافتی به ادمین
    context.bot.send_message(chat_id=ADMIN_ID, text=f"پیام جدید از {update.message.from_user.username}: {update.message.text}")
    update.message.reply_text(f"پیامت دریافت شد!")

# تابع برای ارسال پیام خودکار هر ۲ دقیقه به ایدی خاص
def send_special_message():
    while True:
        try:
            bot.send_message(chat_id=SPECIAL_ID, text=".")
            time.sleep(120)  # ارسال نقطه هر ۲ دقیقه
        except Exception as e:
            logger.error(f"خطا در ارسال پیام ویژه: {e}")
            time.sleep(120)

# تابع برای ارسال پیام ادمین که ربات فعال است
def send_admin_message():
    try:
        bot.send_message(chat_id=ADMIN_ID, text="ربات فعاله!")
    except Exception as e:
        logger.error(f"خطا در ارسال پیام ادمین: {e}")

# تابع برای ارسال پیام صوتی
def send_audio(update: Update, context):
    update.message.reply_audio(audio=open('path_to_audio.mp3', 'rb'))  # مسیر فایل صوتی رو وارد کن

# تابع برای ارسال استیکر
def send_sticker(update: Update, context):
    update.message.reply_sticker(sticker='path_to_sticker')  # مسیر استیکر رو وارد کن

# تابع برای ارسال گیف
def send_gif(update: Update, context):
    update.message.reply_animation(animation='path_to_gif')  # مسیر گیف رو وارد کن

# تابع برای دکمه شیشه‌ای ادمین که به کاربر پیام بده
def send_message_to_user(update: Update, context):
    keyboard = [[InlineKeyboardButton("ارسال پیام به کاربر", callback_data='send_message')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("برای ارسال پیام به کاربر، روی دکمه کلیک کن.", reply_markup=reply_markup)

def button(update: Update, context):
    query = update.callback_query
    if query.data == 'send_message':
        query.answer()
        context.bot.send_message(chat_id=ADMIN_ID, text="پیام به کاربر ارسال شد!")

def main():
    global bot
    bot = Updater(TOKEN, use_context=True).bot  # ذخیره ربات برای ارسال پیام‌ها در تردها
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))  # دستور start
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))  # پیام‌های متنی
    dp.add_handler(MessageHandler(Filters.audio, send_audio))  # ارسال پیام صوتی
    dp.add_handler(MessageHandler(Filters.sticker, send_sticker))  # ارسال استیکر
    dp.add_handler(MessageHandler(Filters.animation, send_gif))  # ارسال گیف
    dp.add_handler(CommandHandler('send_message', send_message_to_user))  # دکمه شیشه‌ای ادمین
    dp.add_handler(CallbackQueryHandler(button))  # دکمه شیشه‌ای ادمین

    # شروع Polling
    updater.start_polling()

    # اجرای ترد جداگانه برای ارسال پیام خودکار هر ۲ دقیقه به ایدی خاص
    threading.Thread(target=send_special_message).start()

    # ارسال پیام ادمین که ربات فعال است (یکبار ارسال)
    send_admin_message()

    updater.idle()  # ربات در حالت idle می‌مونه تا قطع نشه

if __name__ == '__main__':
    main()
