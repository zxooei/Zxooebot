from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram.ext import PicklePersistence
import logging

# تنظیمات اولیه
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن ربات خود را اینجا وارد کنید
TOKEN = "7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo"

# ایدی مدیر ربات (شما)
ADMIN_ID = 5833077341  # ایدی عددی شما رو اینجا وارد کنید!

# دیکشنری برای ذخیره‌سازی وضعیت بلاک
blocked_users = {}

# تابع /start برای شروع مکالمه
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if user.id == ADMIN_ID:
        update.message.reply_text(f"سلام {user.first_name}! چطوری؟ 😄 هر پیامی که دوست داری بفرست، من اینجام که جواب بدم! 🚀")
    else:
        update.message.reply_text(f"سلام {user.first_name}! من یه ربات چت ناشناس هستم. پیام‌های شما رو می‌بینم ولی نمی‌تونم جواب بدم! 😅")

# تابع برای ارسال پیام و نام فرستنده
def handle_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text if update.message.text else "چیزی فرستادی که متن نیست! 🤔"

    # اگر کاربر بلاک نشده باشد
    if user.id not in blocked_users:
        # ارسال پیام به شما با نام فرستنده (فقط برای مدیر)
        if user.id == ADMIN_ID:
            update.message.reply_text(f"👤 {user.first_name} گفت: {text}")
        
        # دکمه‌های شیشه‌ای برای مدیر
        if user.id == ADMIN_ID:
            keyboard = [
                [
                    InlineKeyboardButton("بلاک کن 🚫", callback_data=f"block_{user.id}"),
                    InlineKeyboardButton("پاسخ بدم ✉️", callback_data=f"reply_{user.id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(f"پیامی از {user.first_name} رسید 📬، چیکار کنیم؟", reply_markup=reply_markup)
    else:
        update.message.reply_text(f"اوه! 😬 تو بلاک شدی، نمی‌تونی پیام بدی!")

# تابع بلاک کردن کاربر
def block_user(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    
    # بلاک کردن کاربر
    blocked_users[user_id] = True
    query.answer(f"دیگه خبری از {user_id} نیست! 🚫")
    
    # ارسال پیام به کاربر
    context.bot.send_message(user_id, "تو بلاک شدی. نمی‌تونی پیام بدی 😔")
    query.edit_message_text(text="بلاک شد! 👏")

    # ارسال اطلاعیه به مدیر
    context.bot.send_message(ADMIN_ID, f"آقا/خانم، شما {user_id} رو بلاک کردید! 🔒", reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("باز کن 🔓", callback_data=f"unblock_{user_id}")
    ]]))

# تابع انلاک کردن کاربر
def unblock_user(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    
    # انلاک کردن کاربر
    blocked_users.pop(user_id, None)
    query.answer(f"دیگه بلاک نیست! {user_id} آزاد شد! 🔓")
    
    # ارسال پیام به کاربر
    context.bot.send_message(user_id, "آفرین! تو دوباره می‌تونی پیام بدی 🌟")
    query.edit_message_text(text="آنلاک شد! 🎉")

# تابع ارسال پیام
def reply_to_user(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    
    # ارسال پیام به کاربر
    query.answer()
    query.edit_message_text(text="باشه! حالا هر پیامی که می‌خوای بفرست، من آماده‌ام! ✨")

    # منتظر دریافت پیام از مدیر برای ارسال به کاربر
    context.user_data['reply_to'] = user_id

# دریافت پیام و ارسال به کاربر هدف
def send_reply(update: Update, context: CallbackContext):
    user_id = context.user_data.get('reply_to')
    if user_id:
        # ارسال پیام به کاربر هدف (تمامی انواع پیام‌ها)
        if update.message.text:
            context.bot.send_message(user_id, update.message.text, reply_to_message_id=update.message.message_id)
        elif update.message.sticker:
            context.bot.send_sticker(user_id, update.message.sticker.file_id, reply_to_message_id=update.message.message_id)
        elif update.message.animation:
            context.bot.send_animation(user_id, update.message.animation.file_id, reply_to_message_id=update.message.message_id)
        elif update.message.audio:
            context.bot.send_audio(user_id, update.message.audio.file_id, reply_to_message_id=update.message.message_id)
        elif update.message.video:
            context.bot.send_video(user_id, update.message.video.file_id, reply_to_message_id=update.message.message_id)
        update.message.reply_text("پیام شما ارسال شد! 💬")
        context.user_data['reply_to'] = None
    else:
        update.message.reply_text("هیچ کاربری برای ارسال پیام انتخاب نشده است! 😅")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # استفاده از Persistence برای ذخیره‌سازی اطلاعات
    persistence = PicklePersistence('bot_data')
    updater.persistence = persistence

    # دستورات اصلی
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, send_reply))
    dispatcher.add_handler(CallbackQueryHandler(block_user, pattern='^block_'))
    dispatcher.add_handler(CallbackQueryHandler(unblock_user, pattern='^unblock_'))
    dispatcher.add_handler(CallbackQueryHandler(reply_to_user, pattern='^reply_'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
