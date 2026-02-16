import telebot
import os

TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "بات زنده است! ✅\nتوکن کار میکنه.")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, f"پیامت رسید: {m.text}")

print("بات در حال ران شدن... اگر چیزی ندیدی، لاگ Railway رو چک کن")
bot.polling(none_stop=True, interval=0, timeout=30)