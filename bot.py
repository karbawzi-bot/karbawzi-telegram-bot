from flask import Flask, request
import telebot
import random
import json
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

app = Flask(__name__)

TOKEN = '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w'
bot = telebot.TeleBot(TOKEN, threaded=False)

CHANNEL1 = 'Karbawzi1File'
CHANNEL2 = 'Karbawzi1Trust'
ADMIN_ID = '@Karbawzi1PV'
BOT_USERNAME = 'KarbawziUPDbot'

def fancy_text(t):
    m = {'A':'𝙰','B':'𝙱','C':'𝙲','D':'𝙳','E':'𝙴','F':'𝙵','G':'𝙶','H':'𝙷','I':'𝙸','J':'𝙹','K':'𝙺','L':'𝙻','M':'𝙼','N':'𝙽','O':'𝙾','P':'𝙿','Q':'𝚀','R':'𝚁','S':'𝚂','T':'𝚃','U':'𝚄','V':'𝚅','W':'𝚆','X':'𝚇','Y':'𝚈','Z':'𝚉',
         'a':'𝚊','b':'𝚋','c':'𝚌','d':'𝚍','e':'𝚎','f':'𝚏','g':'𝚐','h':'𝚑','i':'𝚒','j':'𝚓','k':'𝚔','l':'𝚕','m':'𝚖','n':'𝚗','o':'𝚘','p':'𝚙','q':'𝚚','r':'𝚛','s':'𝚜','t':'𝚝','u':'𝚞','v':'𝚟','w':'𝚠','x':'𝚡','y':'𝚢','z':'𝚣'}
    return ''.join(m.get(c, c) for c in t)

MOTIVATION_FA = [
    "「انسان همان‌طور فکر می‌کند که زندگی می‌کند، نه همان‌طور که زندگی می‌کند فکر می‌کند。」 — ریلکه",
    "「عمیق‌ترین چاه‌ها، خاموش‌ترین آب‌ها را دارند。」 — ضرب‌المثل آلمانی",
]
MOTIVATION_EN = [
    "💭 \"We are what we repeatedly do. Excellence, then, is not an act, but a habit.\" — Aristotle",
    "💭 \"The cave you fear to enter holds the treasure you seek.\" — Joseph Campbell",
]

def random_motivation(lang):
    return random.choice(MOTIVATION_FA if lang == 'fa' else MOTIVATION_EN)

DATA_FILE = 'bot_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": {}, "dns_free": {}, "last_motivation": {}}

db = load_data()

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except:
        pass  # اگر ذخیره نشد، ادامه بده

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

def send_new_message(uid, cid, text, reply_markup=None):
    try:
        msg = bot.send_message(cid, text, reply_markup=reply_markup, parse_mode='Markdown')
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        return msg
    except:
        return None

def send_update_message(uid, cid, text):
    try:
        msg = bot.send_message(cid, text, parse_mode='Markdown')
        db["users"][str(uid)]["update_msg_id"] = msg.message_id
        save_data()
        return msg
    except:
        return None

def send_main_menu(uid, cid, lang):
    text = get_text('welcome_main', lang)
    user = get_user(uid)
    
    last = user.get("last_msg")
    if last:
        try:
            bot.edit_message_text(
                text,
                chat_id=cid,
                message_id=last,
                reply_markup=main_menu_keyboard(lang),
                parse_mode='Markdown'
            )
            return
        except:
            pass

    send_new_message(uid, cid, text, main_menu_keyboard(lang))

def get_text(key, lang, **kwargs):
    texts = {
        'promotion': {
            'fa': "✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌\n\n🔥 karbawzi UPD\nفراتر از یه بات ساده...\n\n👤 ادمین: @Karbawzi1PV\n📢 @Karbawzi1File\n🔒 @Karbawzi1Trust",
            'en': fancy_text("✨ KARBAWZI PREMIUM\n\n🔥 karbawzi UPD\nBeyond a simple bot...\n\n👤 Admin: @Karbawzi1PV\n📢 @Karbawzi1File\n🔒 @Karbawzi1Trust")
        },
        'choose_lang': {
            'fa': '🌍 زبان خود را انتخاب کنید:',
            'en': fancy_text('🌍 Select Your Language:')
        },
        'welcome_main': {
            'fa': '✨ به پنل اصلی خوش آمدید! 🚀\n\nلطفاً گزینه مورد نظر را انتخاب کنید.',
            'en': fancy_text('✨ Welcome to Main Panel! 🚀\n\nPlease choose an option.')
        },
        'updating': {
            'fa': '🔄 در حال بروزرسانی...\nلطفاً کمی صبر کنید.',
            'en': fancy_text('🔄 Updating...\nPlease wait a moment.')
        },
        'dns_title': {'fa': '🌐 DNS Servers', 'en': fancy_text('🌐 DNS Servers')},
        'vpn_title': {'fa': '🔒 VPN', 'en': fancy_text('🔒 VPN')},
        'config_update': {
            'fa': '🔄 در حال بروزرسانی کانفیگ...\nبه زودی لینک جدید قرار می‌گیرد.',
            'en': fancy_text('🔄 Config is being updated...\nNew link coming soon.')
        },
        'config_buy': {
            'fa': '💳 خرید اشتراک\n\nبرای خرید با ادمین تماس بگیرید: @Karbawzi1PV',
            'en': fancy_text('💳 Buy Subscription\n\nContact admin: @Karbawzi1PV')
        },
        'wireguard_dns': {
            'fa': '♦️ Wireguard DNS\n\nدر حال خرید بهترین تانل‌ها و آپدیت کامل این بخش از خدمات هستیم.\n\nبه زودی بهترین تجربه را خواهید داشت.',
            'en': fancy_text('♦️ Wireguard DNS\n\nPurchasing the best tunnels and fully updating this service section.\n\nYou will soon have the best experience.')
        },
        'v2ray': {
            'fa': '🚀 V2ray\n\nفعلاً در حال بروزرسانی...\nبه زودی سرورهای جدید.',
            'en': fancy_text('🚀 V2ray\n\nUpdating soon...\nNew servers coming.')
        },
        'currency_title': {
            'fa': '💱 رمزارزها',
            'en': fancy_text('💱 Cryptocurrencies')
        },
        'currency_list': {
            'fa': '🔄 در حال دریافت APIهای رسمی و بروزرسانی داده‌ها...\n\nلطفاً کمی صبور باشید. به زودی قیمت روز و تحلیل ۲۴ ساعته هر رمزارز را تقدیم شما خواهیم کرد.',
            'en': fancy_text('🔄 Receiving official APIs and updating data...\n\nPlease be patient. Soon we will provide daily price and 24-hour analysis for each cryptocurrency.')
        },
        'codm_title': {
            'fa': '🎨 پرامپت عکاسی',
            'en': fancy_text('🎨 Photo Prompt')
        },
        'channels': {
            'fa': '📢 کانال‌های رسمی ما\n\n🔹 <a href="https://t.me/Karbawzi1File">Karbawzi1File</a>\n🔹 <a href="https://t.me/Karbawzi1Trust">Karbawzi1Trust</a>\n🔹 <a href="https://t.me/Karbawzi1PV">Karbawzi1PV</a>\n\nاین بات و کانال‌ها فقط گوشه‌ای از حضور من در وب هست.\nبخش زیادی از من هنوز در تاریکی به سر می‌برد... و قلب سیاهم را فقط معدود نفرات می‌شناسند.',
            'en': fancy_text('📢 Official Channels\n\n🔹 <a href="https://t.me/Karbawzi1File">Karbawzi1File</a>\n🔹 <a href="https://t.me/Karbawzi1Trust">Karbawzi1Trust</a>\n🔹 <a href="https://t.me/Karbawzi1PV">Karbawzi1PV</a>\n\nThis bot & channels are just a corner of my presence on the web.\nMost of me still lives in the darkness... and only a few know my black heart.')
        },
        'sms_bomber': {
            'fa': '💣 Sms Bomber\n\n🔥 در حال توسعه رابط کاربری اختصاصی و فوق حرفه‌ای\n\n🎁 هدیه ویژه: ۵ بمب رایگان برای ۱۰ کاربر اول (به زودی فعال می‌شود)',
            'en': fancy_text('💣 Sms Bomber\n\n🔥 Developing exclusive ultra-professional UI\n\n🎁 Special gift: 5 free bombs for the first 10 users (coming soon)')
        },
        'magic_font': {
            'fa': '✨ Magic Font / زیباسازی متن\n\nمتن خود را وارد کنید (فارسی یا انگلیسی):\n\nپس از ارسال، متن زیباسازی شده را دریافت خواهید کرد.',
            'en': fancy_text('✨ Magic Font\n\nEnter your text (Persian or English):')
        },
        'magic_font_closed': {
            'fa': '🌑 فعلاً این قابلیت بسته است.\n\nبه زودی با نسخه کامل و تاریک بازگشایی می‌شود.',
            'en': fancy_text('🌑 This feature is currently closed.\n\nIt will be opened soon with the full dark version.')
        },
        'public_dns_info': {
            'fa': '🌍 **Public DNS Servers** (لیست کامل و تست‌شده)\n\n• Cloudflare → Primary: `1.1.1.1` | Secondary: `1.0.0.1`\n• Google → Primary: `8.8.8.8` | Secondary: `8.8.4.4`\n• Quad9 → Primary: `9.9.9.9` | Secondary: `149.112.112.112`\n• OpenDNS → Primary: `208.67.222.222` | Secondary: `208.67.220.220`\n• Level3 → Primary: `209.244.0.3` | Secondary: `209.244.0.4`\n• Comodo Secure → Primary: `8.26.56.26` | Secondary: `8.20.247.20`\n• AdGuard → Primary: `94.140.14.14` | Secondary: `94.140.15.15`\n• NextDNS → Primary: `45.90.28.0` | Secondary: `45.90.30.0`\n\n💡 **چگونه استفاده کنید؟**\n• **اندروید**: برنامه DNS Changer از گوگل پلی نصب کنید → IPها را وارد کنید\n• **iOS**: به Settings → Wi-Fi بروید → روی i (اطلاعات) شبکه کلیک کنید → DNS را روی Manual بگذارید → IPها را اضافه کنید\n\n**نکته مهم APN**: در حال حاضر شرایط کشور ایجاب می‌کنه از طریق سیم‌کارت به بخش APN برید و از حالت دوطرفه IPv4/IPv6 به حالت IPv4 انحصاری تغییر بدید.',
            'en': fancy_text('🌍 **Public DNS Servers** (Complete & Tested List)\n\n• Cloudflare → Primary: `1.1.1.1` | Secondary: `1.0.0.1`\n• Google → Primary: `8.8.8.8` | Secondary: `8.8.4.4`\n• Quad9 → Primary: `9.9.9.9` | Secondary: `149.112.112.112`\n• OpenDNS → Primary: `208.67.222.222` | Secondary: `208.67.220.220`\n• Level3 → Primary: `209.244.0.3` | Secondary: `209.244.0.4`\n• Comodo Secure → Primary: `8.26.56.26` | Secondary: `8.20.247.20`\n• AdGuard → Primary: `94.140.14.14` | Secondary: `94.140.15.15`\n• NextDNS → Primary: `45.90.28.0` | Secondary: `45.90.30.0`\n\n💡 **How to use?**\n• **Android**: Install DNS Changer from Google Play → Enter IPs\n• **iOS**: Settings → Wi-Fi → i → DNS Manual → Add IPs\n\n**APN Note**: In current conditions, go to APN settings via SIM card and change from dual IPv4/IPv6 to IPv4 only.')
        },
        'cloud_dns_info': {
            'fa': '☁️ **Cloud DNS**\n\nاین یکی از بهترین تجربه‌های شما از DNS می‌تواند باشه.\nدر حال حاضر در حال بررسی و ست کردن IPهای جدید در بات هستیم.\nبزودی خیلی از گزینه‌ها براتون باز خواهند شد و سرعت و پایداری بی‌نظیری تجربه خواهید کرد.',
            'en': fancy_text('☁️ **Cloud DNS**\n\nThis can be one of your best DNS experiences.\nWe are currently testing and setting new IPs in the bot.\nSoon many options will be opened for you with unparalleled speed and stability.')
        },
    }
    return texts.get(key, {}).get(lang, '🔄 در حال آماده‌سازی...').format(**kwargs)

def main_menu_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = [
            "🎨 پرامپت عکاسی", "💱 رمزارزها",
            "🌐 DNS Servers", "🔒 VPN",
            "📢 کانال‌ها", "💣 Sms Bomber"
        ]
    else:
        buttons = [fancy_text(b) for b in [
            "🎨 Photo Prompt", "💱 Cryptocurrencies",
            "🌐 DNS Servers", "🔒 VPN",
            "📢 Channels", "💣 Sms Bomber"
        ]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🌍 تغییر زبان"))
    return markup

def prompt_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = ["📤 ارسال پرامپت", "📥 دریافت پرامپت"]
    else:
        buttons = [fancy_text(b) for b in ["📤 Send Prompt", "📥 Receive Prompt"]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def dns_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = ["☁️ Cloud DNS", "♦️ Wireguard DNS", "🌍 Public DNS"]
    else:
        buttons = [fancy_text(b) for b in ["☁️ Cloud DNS", "♦️ Wireguard DNS", "🌍 Public DNS"]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def vpn_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = ["🚀 V2ray", "♦️ Wireguard"]
    else:
        buttons = [fancy_text(b) for b in ["🚀 V2ray", "♦️ Wireguard"]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def currency_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = ["₿ Bitcoin", "⟠ Ethereum", "🔶 Solana", "❎ XRP", "🐶 Dogecoin", "🔶 BNB", "🌟 Cardano", "🔗 Chainlink"]
    else:
        buttons = [fancy_text(b) for b in ["₿ Bitcoin", "⟠ Ethereum", "🔶 Solana", "❎ XRP", "🐶 Dogecoin", "🔶 BNB", "🌟 Cardano", "🔗 Chainlink"]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def get_button_action(text, lang):
    actions = {
        'fa': {
            "🎨 پرامپت عکاسی": "prompt_menu",
            "💱 رمزارزها": "currency",
            "🌐 DNS Servers": "dns_menu",
            "🔒 VPN": "vpn_menu",
            "📢 کانال‌ها": "channels",
            "💣 Sms Bomber": "sms_bomber",
            "☁️ Cloud DNS": "dns_cloud",
            "♦️ Wireguard DNS": "wireguard_dns",
            "🌍 Public DNS": "dns_public",
            "🚀 V2ray": "v2ray",
            "♦️ Wireguard": "wireguard",
            "📤 ارسال پرامپت": "prompt_send",
            "📥 دریافت پرامپت": "prompt_receive",
            "🌍 تغییر زبان": "change_lang",
        },
        'en': {fancy_text(k): v for k, v in {
            "🎨 Photo Prompt": "prompt_menu",
            "💱 Cryptocurrencies": "currency",
            "🌐 DNS Servers": "dns_menu",
            "🔒 VPN": "vpn_menu",
            "📢 Channels": "channels",
            "💣 Sms Bomber": "sms_bomber",
            "☁️ Cloud DNS": "dns_cloud",
            "♦️ Wireguard DNS": "wireguard_dns",
            "🌍 Public DNS": "dns_public",
            "🚀 V2ray": "v2ray",
            "♦️ Wireguard": "wireguard",
            "🌍 Change Language": "change_lang",
        }.items()}
    }
    return actions.get(lang, {}).get(text.strip())

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    cid = m.chat.id
    user = get_user(uid)
    text = get_text('promotion', 'fa') + "\n\n" + get_text('promotion_footer_fa', 'fa')
    send_new_message(uid, cid, text, language_keyboard())
    user["has_seen_welcome"] = True
    save_data()

@bot.message_handler(func=lambda m: True)
def handle_messages(m):
    uid = m.from_user.id
    cid = m.chat.id
    text = m.text.strip()
    user = get_user(uid)
    lang = user.get("lang", 'fa')
    action = get_button_action(text, lang)

    if text in ['🇮🇷 فارسی', '🇬🇧 English']:
        new_lang = 'fa' if text == '🇮🇷 فارسی' else 'en'
        update_user(uid, {"lang": new_lang})
        lang = new_lang
        send_main_menu(uid, cid, lang)
        return

    if "برگشت" in text or "Back" in text:
        send_main_menu(uid, cid, lang)
        return

    if action == "prompt_menu":
        send_new_message(uid, cid, get_text('prompt_title', lang), prompt_keyboard(lang))
        return

    elif action in ["prompt_send", "prompt_receive"]:
        send_update_message(uid, cid, get_text('prompt_closed', lang))
        return

    if action == "currency":
        send_new_message(uid, cid, get_text('currency_title', lang), currency_keyboard(lang))
        return

    elif action.startswith("crypto_"):
        send_update_message(uid, cid, get_text('currency_info', lang))
        return

    elif action == "dns_menu":
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
        return

    elif action == "dns_public":
        send_update_message(uid, cid, get_text('public_dns_info', lang))
        return

    elif action == "dns_cloud":
        send_update_message(uid, cid, get_text('cloud_dns_info', lang))
        return

    elif action == "wireguard_dns":
        send_update_message(uid, cid, get_text('wireguard_dns', lang))
        return

    elif action == "vpn_menu":
        send_new_message(uid, cid, get_text('vpn_title', lang), vpn_keyboard(lang))
        return

    elif action in ["v2ray", "wireguard"]:
        send_update_message(uid, cid, get_text('vpn_message', lang))
        return

    elif action == "channels":
        send_update_message(uid, cid, get_text('channels', lang))
        return

    elif action == "sms_bomber":
        send_update_message(uid, cid, get_text('sms_bomber', lang))
        return

    send_update_message(uid, cid, get_text('updating', lang))
    send_main_menu(uid, cid, lang)

@app.route('/')
def home():
    return "بات Karbawzi webhook فعال است! 🚀"

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return 'OK', 200
        else:
            return 'Bad request', 403
    except Exception as e:
        print(f"Webhook error: {e}")
        return 'OK', 200

application = app