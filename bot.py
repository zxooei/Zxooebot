from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import logging
import threading
import time

# تنظیمات ربات
TOKEN = '7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo'  # توکن ربات خود را اینجا قرار بدهید
ADMIN_ID = 5833077341  # آیدی ادمین را اینجا وارد کنید
SPECIAL_ID = 7248220184  # آیدی خاص که ربات هر 2 دقیقه برای آن پیام بفرستد

# لاگ‌ها برای بررسی خطا
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# پیام شروع
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! پیامتو بفرست تا برسه دستم!")

# ارسال دکمه پاسخ فقط برای ادمین
def send_to_admin_with_button(bot, message, user_id):
    user_name = message.from_user.full_name  # اسم کامل کاربر
    user_username = message.from_user.username  # نام کاربری (در صورت موجود بودن)
    user_id = message.from_user.id  # آیدی کاربر
    
    # فوروارد کردن پیام به ادمین
    forward = bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat_id, message_id=message.message_id)
    
    keyboard = [
        [InlineKeyboardButton("پاسخ به این پیام", callback_data=f"reply|{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ارسال پیام به ادمین با نمایش اسم، نام کاربری و آیدی کاربر
    bot.send_message(
        chat_id=ADMIN_ID,
        text=f"پیامی از {user_name} (@{user_username}) رسید.\n\nID: {user_id}\n\nبا کلیک روی دکمه زیر می‌تونی بهش پاسخ بدی.",
        reply_markup=reply_markup
    )

# هندل همه‌ی نوع پیام
def handle_all_messages(update: Update, context: CallbackContext):
    message = update.message
    user_id = message.from_user.id

    # بررسی اینکه آیا فرستنده همان ادمین است یا خیر
    if message.chat_id == ADMIN_ID:
        return  # اگر ادمین پیام بده، پیام دوباره برای خود ادمین ارسال نشود

    # ارسال پیام به ادمین
    send_to_admin_with_button(context.bot, message, user_id)
    
    # ارسال پیام تایید به کاربر
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
    
    # پیدا کردن آیدی کاربر هدف از context
    target = context.user_data.get("reply_to")
    
    # بررسی اینکه آیا آیدی هدف مشخص شده یا خیر
    if target:
        # ارسال پیام به کاربر هدف (نه به ادمین)
        context.bot.send_message(
            chat_id=target, 
            text=f"پیام جدید از ادمین:\n\n{update.message.text}"
        )
        # تایید ارسال پیام به ادمین
        update.message.reply_text("پیام به کاربر ارسال شد!")
        
        # پاک کردن آیدی هدف از context بعد از ارسال
        context.user_data["reply_to"] = None
    else:
        update.message.reply_text("اول باید رو دکمه‌ی «پاسخ به این پیام» بزنی!")

# ارسال نقطه هر 2 دقیقه به SPECIAL_ID
def keep_bot_alive():
    while True:
        try:
            bot.send_message(chat_id=SPECIAL_ID, text=".")
        except Exception as e:
            logger.error(f"خطا در keep_alive: {e}")
        time.sleep(120)

# ارسال پیام وضعیت ربات برای ادمین
def send_bot_status_message(status):
    try:
        bot.send_message(chat_id=ADMIN_ID, text=f"وضعیت ربات: {status}")
    except Exception as e:
        logger.error(f"خطا در ارسال وضعیت ربات: {e}")

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

    # ارسال پیام وضعیت ربات به ادمین
    send_bot_status_message("در حال راه‌اندازی...")
    
    updater.start_polling()  # ربات شروع به کار می‌کند
    send_bot_status_message("فعال است.")  # اطلاع از فعال بودن ربات
    
    updater.idle()  # منتظر دریافت پیام‌ها

    send_bot_status_message("خاموش شد.")  # اطلاع از خاموش بودن ربات

if __name__ == '__main__':
    main()
