import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')

channel1 = 'Karbawzi1File'
channel2 = 'Karbawzi1Trust'

files = {
    'ProMax': 'https://drive.google.com/uc?export=download&id=1pFyOgtExpPRdr1ifk7M9CEDNSBfvp8kf',
    'TopVIP': 'https://drive.google.com/uc?export=download&id=1XOXH9HE8lDSm8W1oTpkT3I0CdtguxDsW',
    'YouTuber': 'https://drive.google.com/uc?export=download&id=1WgxegdnxMgHFfI_cOjmbR2x5i27hCHnW'
}

def is_member(user_id):
    try:
        status1 = bot.get_chat_member(f'@{channel1}', user_id).status
        status2 = bot.get_chat_member(f'@{channel2}', user_id).status
        return status1 in ['member', 'administrator', 'creator'] and status2 in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"خطا چک عضویت: {e}")
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_member(user_id):
        send_panel(message.chat.id)
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("جوین کانال فایل‌ها 📁", url=f'https://t.me/{channel1}'))
        markup.add(InlineKeyboardButton("جوین کانال اعتماد 🔒", url=f'https://t.me/{channel2}'))
        markup.add(InlineKeyboardButton("بررسی عضویت ✅", callback_data='check'))
        bot.send_message(message.chat.id, "سلام! برای دسترسی، اول در دو کانال جوین شو 🚀", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'check':
        if is_member(call.from_user.id):
            bot.answer_callback_query(call.id, "عضویت تایید شد! حالا دانلود کن ✓")
            send_panel(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "هنوز جوین نشدی 😕", show_alert=True)
    elif call.data in files:
        try:
            bot.send_document(call.message.chat.id, files[call.data])
            bot.answer_callback_query(call.id, "فایل ارسال شد! دانلود شروع شد 🚀")
        except Exception as e:
            bot.send_message(call.message.chat.id, "خطا در ارسال فایل! لینک رو چک کن یا بعدا امتحان کن 😔")
            print(f"خطا ارسال: {e}")

def send_panel(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("📥 ProMax - آخرین نسخه", callback_data='ProMax'))
    markup.add(InlineKeyboardButton("📥 TopVIP - آخرین نسخه", callback_data='TopVIP'))
    markup.add(InlineKeyboardButton("📥 YouTuber - آخرین نسخه", callback_data='YouTuber'))
    bot.send_message(chat_id, "به پنل خوش اومدی 🔥\nیکی رو انتخاب کن:", reply_markup=markup)

print("بات آنلاین شد!")
bot.polling(none_stop=True, interval=0, timeout=30)
