import telebot
import os
import random
import json
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')
bot = telebot.TeleBot(TOKEN)

CHANNEL1 = 'Karbawzi1File'
CHANNEL2 = 'Karbawzi1Trust'
ADMIN_ID = '@Karbawzi1PV'
BOT_USERNAME = 'KarbawziUPDbot'

def fancy(t):
    m = {'A':'𝙰','B':'𝙱','C':'𝙲','D':'𝙳','E':'𝙴','F':'𝙵','G':'𝙶','H':'𝙷','I':'𝙸','J':'𝙹','K':'𝙺','L':'𝙻','M':'𝙼','N':'𝙽','O':'𝙾','P':'𝙿','Q':'𝚀','R':'𝚁','S':'𝚂','T':'𝚃','U':'𝚄','V':'𝚅','W':'𝚆','X':'𝚇','Y':'𝚈','Z':'𝚉',
         'a':'𝚊','b':'𝚋','c':'𝚌','d':'𝚍','e':'𝚎','f':'𝚏','g':'𝚐','h':'𝚑','i':'𝚒','j':'𝚓','k':'𝚔','l':'𝚕','m':'𝚖','n':'𝚗','o':'𝚘','p':'𝚙','q':'𝚚','r':'𝚛','s':'𝚜','t':'𝚝','u':'𝚞','v':'𝚟','w':'𝚠','x':'𝚡','y':'𝚢','z':'𝚣'}
    return ''.join(m.get(c, c) for c in t)

# داده‌ها
DATA_FILE = 'bot_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": {}, "dns_free": {}, "last_motivation": {}}

db = load_data()

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {
            "lang": "fa",
            "ref_code": f"ref{uid}",
            "referred_by": None,
            "referrals_list": [],
            "claimed": {"free_account":False,"artery":False,"vivan":False,"youtuber":False,"freefile":False,"free_codm":False},
            "last_msg": None,
            "has_seen_welcome": False,
            "current_menu": "main"
        }
        save_data()
    return db["users"][uid]

def update_user(uid, data):
    db["users"][str(uid)].update(data)
    save_data()

def is_member(uid):
    try:
        s1 = bot.get_chat_member(f'@{CHANNEL1}', uid).status
        s2 = bot.get_chat_member(f'@{CHANNEL2}', uid).status
        return s1 in ['member','administrator','creator'] and s2 in ['member','administrator','creator']
    except:
        return False

def count_successful_referrals(uid):
    c = 0
    for ref in db["users"][str(uid)].get("referrals_list", []):
        if is_member(int(ref)):
            c += 1
    return c

def add_referral(rid, nid):
    rid, nid = str(rid), str(nid)
    if rid == nid: return
    if nid not in db["users"][rid].get("referrals_list", []):
        db["users"][rid]["referrals_list"].append(nid)
        save_data()

# ────────────────────────────────────────────────
# ارسال پیام (بدون پاک کردن)

def send_message(cid, text, reply_markup=None):
    return bot.send_message(cid, text, reply_markup=reply_markup, parse_mode='Markdown')

def send_main_menu(uid, cid, lang):
    user = get_user(uid)
    text = "✨ به پنل اصلی خوش آمدید! 🚀\n\nلطفاً گزینه مورد نظر را انتخاب کنید." if lang == 'fa' else fancy("✨ Welcome to Main Panel! 🚀\n\nPlease choose an option.")

    last = user.get("last_msg")
    if last:
        try:
            bot.edit_message_text(text, cid, last, reply_markup=main_menu_keyboard(lang), parse_mode='Markdown')
            return
        except:
            pass

    msg = send_message(cid, text, main_menu_keyboard(lang))
    user["last_msg"] = msg.message_id
    save_data()

# ────────────────────────────────────────────────
# کیبوردهای حرفه‌ای

def main_menu_keyboard(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        btns = ["🎮 Codm Config", "💱 قیمت ارز", "🎬 گیم پلی", "🌐 DNS + Wireguard", "🔒 VPN", "🆓 کالاف دیوتی", "🌍 تغییر زبان", "📢 کانال‌ها"]
    else:
        btns = [fancy(b) for b in ["🎮 Codm Config", "💱 Currency Prices", "🎬 Gameplay", "🌐 DNS + Wireguard", "🔒 VPN", "🆓 CODM", "🌍 Change Language", "📢 Channels"]]
    m.add(*[KeyboardButton(b) for b in btns])
    return m

def codm_config_keyboard(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        btns = ["🚀 ProMax", "👑 TopVIP", "📺 Youtuber", "🆓 FreeFile"]
    else:
        btns = [fancy(b) for b in ["🚀 ProMax", "👑 TopVIP", "📺 Youtuber", "🆓 FreeFile"]]
    m.add(*[KeyboardButton(b) for b in btns])
    m.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy("🔙 Back to Main Menu")))
    return m

def config_action_keyboard(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        btns = ["📥 دریافت آپدیت", "💳 خرید اشتراک"]
    else:
        btns = [fancy(b) for b in ["📥 Get Update", "💳 Buy Subscription"]]
    m.add(*[KeyboardButton(b) for b in btns])
    m.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy("🔙 Back to Main Menu")))
    return m

def dns_keyboard(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        btns = ["📶 ایرانسل", "📶 همراه اول", "📶 مخابرات", "📶 شاتل", "🌍 Public DNS", "🧪 Free Test", "🔐 Wireguard DNS", "🔐 Wireguard VPN"]
    else:
        btns = [fancy(b) for b in ["📶 Irancell", "📶 MCI", "📶 Mokhaberat", "📶 Shatel", "🌍 Public DNS", "🧪 Free Test", "🔐 Wireguard DNS", "🔐 Wireguard VPN"]]
    m.add(*[KeyboardButton(b) for b in btns])
    m.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy("🔙 Back to Main Menu")))
    return m

def vpn_keyboard(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        btns = ["🔐 Wireguard", "🚀 V2ray"]
    else:
        btns = [fancy(b) for b in ["🔐 Wireguard", "🚀 V2ray"]]
    m.add(*[KeyboardButton(b) for b in btns])
    m.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy("🔙 Back to Main Menu")))
    return m

def currency_keyboard(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    m.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy("🔙 Back to Main Menu")))
    return m

# ────────────────────────────────────────────────
# متن‌ها

def get_text(key, lang, **kwargs):
    data = {
        'welcome_main': {
            'fa': '✨ به پنل اصلی خوش آمدید! 🚀\n\nلطفاً گزینه مورد نظر را انتخاب کنید.',
            'en': fancy('✨ Welcome to Main Panel! 🚀\n\nPlease choose an option.')
        },
        'updating': {
            'fa': '🔄 در حال بروزرسانی...\nلطفاً کمی صبر کنید.',
            'en': fancy('🔄 Updating...\nPlease wait a moment.')
        },
        'config_update': {'fa': '🔄 در حال بروزرسانی کانفیگ...\nبه زودی لینک جدید قرار می‌گیرد.', 'en': fancy('🔄 Config is being updated...\nNew link coming soon.')},
        'config_buy': {'fa': '💳 خرید اشتراک\n\nبرای خرید با ادمین تماس بگیرید: @Karbawzi1PV', 'en': fancy('💳 Buy Subscription\n\nContact admin: @Karbawzi1PV')},
    }
    return data.get(key, {}).get(lang, '')

# ────────────────────────────────────────────────
# handler اصلی

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    cid = m.chat.id
    user = get_user(uid)

    if len(m.text.split()) > 1 and m.text.split()[1].startswith('ref'):
        rid = m.text.split()[1][3:]
        if rid != str(uid):
            add_referral(rid, uid)

    if not user["has_seen_welcome"]:
        send_message(cid, "✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌\n\n🔥 karbawzi UPD\nفراتر از یه بات ساده...\n\n👤 ادمین: @Karbawzi1PV\n📢 @Karbawzi1File\n🔒 @Karbawzi1Trust", language_keyboard())
    else:
        send_main_menu(uid, cid, user["lang"])

@bot.message_handler(func=lambda m: True)
def handle(m):
    uid = m.from_user.id
    cid = m.chat.id
    text = m.text.strip()
    user = get_user(uid)
    lang = user["lang"]
    t = text.lower()

    # برگشت به منوی اصلی
    if "برگشت" in text or "back" in t:
        send_main_menu(uid, cid, lang)
        return

    # Codm Config
    if "codm" in t or "کالاف" in t or "config" in t:
        send_message(cid, "انتخاب کانفیگ:", codm_config_keyboard(lang))
        return

    # زیرمنوهای Codm
    if any(x in t for x in ["promax", "topvip", "youtuber", "freefile", "پرومکس", "تاپ", "یوتیوبر", "فری", "pro", "top", "youtuber", "free"]):
        send_message(cid, "عملیات:", config_action_keyboard(lang))
        return

    # دریافت آپدیت و خرید
    if "آپدیت" in text or "update" in t:
        send_message(cid, get_text('config_update', lang))
        return
    if "خرید" in text or "buy" in t or "subscription" in t:
        send_message(cid, get_text('config_buy', lang))
        return

    # DNS + Wireguard
    if "dns" in t or "دی ان اس" in t or "wireguard" in t:
        send_message(cid, get_text('dns_title', lang) if 'dns_title' in get_text else "🌐 DNS + Wireguard", dns_keyboard(lang))
        return

    # VPN
    if "vpn" in t or "وی پی ان" in t:
        send_message(cid, get_text('vpn_title', lang) if 'vpn_title' in get_text else "🔒 VPN", vpn_keyboard(lang))
        return

    # قیمت ارز
    if "ارز" in t or "currency" in t or "prices" in t:
        send_message(cid, "💱 قیمت ارزها (انگلیسی)", currency_keyboard(lang))
        send_message(cid, "لیست کامل ارزها در حال بروزرسانی...")
        return

    # تغییر زبان
    if "تغییر زبان" in text or "change language" in t:
        send_message(cid, get_text('choose_lang', lang), language_keyboard())
        return

    send_message(cid, "❌ دستور نامعتبر است.\nلطفاً از دکمه‌های کیبورد استفاده کنید.")

print("🚀 Karbawzi UPD Bot - نسخه حرفه‌ای و تمیز")
bot.polling(none_stop=True, interval=0, timeout=30)