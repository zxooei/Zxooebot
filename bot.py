import telebot

TOKEN = "7759629156:AAEVdRZSUa8AONPKDUHJdOReUosR3LT5fRo"
ADMIN_ID = 5833077341  # آیدی عددی شما

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "هرچی دوست داری بگو")

@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

bot.polling()