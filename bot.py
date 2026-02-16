import telebot
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'test'])
def test(m):
    bot.reply_to(m, "بات زنده است! ✅\nاگر این پیام رو دیدی یعنی همه چیز درست کار می‌کنه.")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, f"پیامت رسید: {m.text}")

print("بات شروع به کار کرد...")
bot.polling(none_stop=True)