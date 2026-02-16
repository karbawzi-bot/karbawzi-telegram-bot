import telebot
import os

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("توکن پیدا نشد! BOT_TOKEN رو در Variables بگذار.")
    exit(1)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'ping'])
def ping(m):
    bot.reply_to(m, "بات زنده است! ✅\nتوکن کار می‌کنه و دستور دریافت شد.")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, f"پیامت رسید: {m.text}")

print("بات شروع به کار کرد... منتظر دستور /start یا /ping هستم")
bot.polling(none_stop=True, interval=0, timeout=30)