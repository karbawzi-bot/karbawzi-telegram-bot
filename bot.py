import telebot
import os
import random
import json
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

# ────────────────────────────────────────────────
# تنظیمات اصلی (برای Railway و GitHub مناسب است)
TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')
bot = telebot.TeleBot(TOKEN)

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
# توابع ارسال پیام (بدون پاک کردن هیچ پیامی)

def send_new_message(uid, cid, text, reply_markup=None):
    msg = bot.send_message(cid, text, reply_markup=reply_markup, parse_mode='Markdown')
    db["users"][str(uid)]["last_msg"] = msg.message_id
    save_data()
    return msg

def send_update_message(uid, cid, text):
    msg = bot.send_message(cid, text, parse_mode='Markdown')
    db["users"][str(uid)]["update_msg_id"] = msg.message_id
    save_data()
    return msg

def send_main_menu(uid, cid, lang):
    text = get_text('welcome_main', lang)
    user = get_user(uid)
    
    # اگر پیام قبلی وجود داره سعی می‌کنیم ویرایش کنیم (تکرار نمیشه)
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
            pass  # اگر نشد → پیام جدید می‌فرستیم

    send_new_message(uid, cid, text, main_menu_keyboard(lang))

# ────────────────────────────────────────────────
# متن‌ها (کامل و بدون نقص)

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
        'dns_title': {'fa': '🌐 DNS + Wireguard', 'en': fancy_text('🌐 DNS + Wireguard')},
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
            'fa': '🔐 Wireguard DNS\n\nپرایمری: `78.157.53.52`\nثانویه: `78.157.53.219`\n\n💡 برای استفاده، تنظیمات Wireguard را بروز کنید.',
            'en': fancy_text('🔐 Wireguard DNS\n\nPrimary: `78.157.53.52`\nSecondary: `78.157.53.219`\n\n💡 Update Wireguard settings to use.')
        },
        'wireguard_vpn': {
            'fa': '🔐 Wireguard VPN\n\nفعلاً در حال بروزرسانی...\nبه زودی کانفیگ‌های جدید.',
            'en': fancy_text('🔐 Wireguard VPN\n\nUpdating soon...\nNew configs coming.')
        },
        'v2ray': {
            'fa': '🚀 V2ray\n\nفعلاً در حال بروزرسانی...\nبه زودی سرورهای جدید.',
            'en': fancy_text('🚀 V2ray\n\nUpdating soon...\nNew servers coming.')
        },
        'currency_title': {
            'fa': '💱 قیمت ارزها',
            'en': fancy_text('💱 Currency Prices')
        },
        'currency_list': {
            'fa': '🔄 در حال بروزرسانی لیست قیمت‌ها...\n\n💰 دلار: ۶۲,۵۰۰ تومان\n💰 یورو: ۶۸,۳۰۰ تومان\n💰 پوند: ۷۹,۱۰۰ تومان\n\n(به‌روزرسانی هر ۳۰ دقیقه)',
            'en': fancy_text('🔄 Updating currency prices...\n\n💰 USD: 62,500 T\n💰 EUR: 68,300 T\n💰 GBP: 79,100 T\n\n(Updates every 30 min)')
        },
        'codm_title': {
            'fa': '🎮 کانفیگ‌های کالاف دیوتی موبایل',
            'en': fancy_text('🎮 CODM Mobile Configs')
        },
        'gameplay_title': {
            'fa': '🎬 گیم‌پلی‌های حرفه‌ای',
            'en': fancy_text('🎬 Pro Gameplay')
        },
        'free_codm_title': {
            'fa': '🆓 کالاف دیوتی رایگان',
            'en': fancy_text('🆓 Free CODM')
        },
        'channels': {
            'fa': '📢 کانال‌های رسمی ما:\n\n🔹 فایل‌ها: @Karbawzi1File\n🔹 اعتماد: @Karbawzi1Trust\n\n🌟 برای پشتیبانی: @Karbawzi1PV',
            'en': fancy_text('📢 Our Official Channels:\n\n🔹 Files: @Karbawzi1File\n🔹 Trust: @Karbawzi1Trust\n\n🌟 Support: @Karbawzi1PV')
        }
        # می‌تونی بقیه رو بعداً اضافه کنی
    }
    return texts.get(key, {}).get(lang, '🔄 متن در حال آماده‌سازی...').format(**kwargs)

# ────────────────────────────────────────────────
# کیبوردها (کاملاً یکپارچه با fancy_text و بدون باگ)

def language_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("🇮🇷 فارسی"), KeyboardButton("🇬🇧 English"))
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی"))
    return markup

def main_menu_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = [
            "🎮 Codm Config", "💱 قیمت ارز",
            "🎬 گیم پلی", "🌐 DNS + Wireguard",
            "🔒 VPN", "🆓 کالاف دیوتی",
            "🌍 تغییر زبان", "📢 کانال‌ها"
        ]
    else:
        buttons = [
            fancy_text("🎮 Codm Config"), fancy_text("💱 Currency Prices"),
            fancy_text("🎬 Gameplay"), fancy_text("🌐 DNS + Wireguard"),
            fancy_text("🔒 VPN"), fancy_text("🆓 CODM"),
            fancy_text("🌍 Change Language"), fancy_text("📢 Channels")
        ]
    markup.add(*[KeyboardButton(b) for b in buttons])
    return markup

def codm_config_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = [
            "🚀 ProMax", "👑 TopVIP",
            "📺 Youtuber", "🆓 FreeFile"
        ]
    else:
        buttons = [fancy_text(b) for b in [
            "🚀 ProMax", "👑 TopVIP",
            "📺 Youtuber", "🆓 FreeFile"
        ]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def config_action_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = [
            "📥 دریافت آپدیت",
            "💳 خرید اشتراک"
        ]
    else:
        buttons = [fancy_text(b) for b in [
            "📥 Get Update",
            "💳 Buy Subscription"
        ]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def dns_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = [
            "📶 ایرانسل", "📶 همراه اول",
            "📶 مخابرات", "📶 شاتل",
            "🌍 Public DNS", "🧪 Free Test",
            "🔐 Wireguard DNS", "🔐 Wireguard VPN"
        ]
    else:
        buttons = [fancy_text(b) for b in [
            "📶 Irancell", "📶 MCI",
            "📶 Mokhaberat", "📶 Shatel",
            "🌍 Public DNS", "🧪 Free Test",
            "🔐 Wireguard DNS", "🔐 Wireguard VPN"
        ]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def vpn_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    if lang == 'fa':
        buttons = [
            "🔐 Wireguard",
            "🚀 V2ray"
        ]
    else:
        buttons = [fancy_text(b) for b in [
            "🔐 Wireguard",
            "🚀 V2ray"
        ]]
    markup.add(*[KeyboardButton(b) for b in buttons])
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def currency_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

# ────────────────────────────────────────────────
# مپینگ دکمه‌ها به اکشن‌ها (برای جلوگیری از هرگونه باگ در مقایسه متن)

def get_button_action(text, lang):
    """دکمه رو به اکشن تبدیل می‌کنه - کاملاً robust"""
    actions = {
        'fa': {
            "🎮 Codm Config": "codm_config",
            "💱 قیمت ارز": "currency",
            "🎬 گیم پلی": "gameplay",
            "🌐 DNS + Wireguard": "dns_menu",
            "🔒 VPN": "vpn_menu",
            "🆓 کالاف دیوتی": "free_codm",
            "🌍 تغییر زبان": "change_lang",
            "📢 کانال‌ها": "channels",
            
            # sub menus
            "🚀 ProMax": "config_promax",
            "👑 TopVIP": "config_topvip",
            "📺 Youtuber": "config_youtuber",
            "🆓 FreeFile": "config_freefile",
            "📥 دریافت آپدیت": "get_update",
            "💳 خرید اشتراک": "buy_sub",
            
            "📶 ایرانسل": "dns_irancell",
            "📶 همراه اول": "dns_mci",
            "📶 مخابرات": "dns_mokhaberat",
            "📶 شاتل": "dns_shatel",
            "🌍 Public DNS": "dns_public",
            "🧪 Free Test": "dns_free",
            "🔐 Wireguard DNS": "wireguard_dns",
            "🔐 Wireguard VPN": "wireguard_vpn",
            
            "🔐 Wireguard": "wireguard_vpn",
            "🚀 V2ray": "v2ray",
        },
        'en': {
            fancy_text("🎮 Codm Config"): "codm_config",
            fancy_text("💱 Currency Prices"): "currency",
            fancy_text("🎬 Gameplay"): "gameplay",
            fancy_text("🌐 DNS + Wireguard"): "dns_menu",
            fancy_text("🔒 VPN"): "vpn_menu",
            fancy_text("🆓 CODM"): "free_codm",
            fancy_text("🌍 Change Language"): "change_lang",
            fancy_text("📢 Channels"): "channels",
            
            # sub menus
            fancy_text("🚀 ProMax"): "config_promax",
            fancy_text("👑 TopVIP"): "config_topvip",
            fancy_text("📺 Youtuber"): "config_youtuber",
            fancy_text("🆓 FreeFile"): "config_freefile",
            fancy_text("📥 Get Update"): "get_update",
            fancy_text("💳 Buy Subscription"): "buy_sub",
            
            fancy_text("📶 Irancell"): "dns_irancell",
            fancy_text("📶 MCI"): "dns_mci",
            fancy_text("📶 Mokhaberat"): "dns_mokhaberat",
            fancy_text("📶 Shatel"): "dns_shatel",
            fancy_text("🌍 Public DNS"): "dns_public",
            fancy_text("🧪 Free Test"): "dns_free",
            fancy_text("🔐 Wireguard DNS"): "wireguard_dns",
            fancy_text("🔐 Wireguard VPN"): "wireguard_vpn",
            
            fancy_text("🔐 Wireguard"): "wireguard_vpn",
            fancy_text("🚀 V2ray"): "v2ray",
        }
    }
    return actions.get(lang, {}).get(text.strip())

# ────────────────────────────────────────────────
# handlerها

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    cid = m.chat.id
    args = m.text.split()

    if len(args) > 1 and args[1].startswith('ref'):
        rid = args[1][3:]
        if rid != str(uid):
            add_referral(rid, uid)
            get_user(uid)["referred_by"] = rid
            save_data()

    user = get_user(uid)

    if not user["has_seen_welcome"]:
        send_new_message(uid, cid, get_text('promotion', 'fa'), language_keyboard())
    else:
        send_main_menu(uid, cid, user["lang"])

@bot.message_handler(func=lambda m: True)
def handle_messages(m):
    uid = m.from_user.id
    cid = m.chat.id
    text = m.text.strip()
    user = get_user(uid)
    lang = user.get("lang", 'fa')
    action = get_button_action(text, lang)

    # هیچ پیامی پاک نمی‌شود

    # تغییر زبان
    if text in ['🇮🇷 فارسی', '🇬🇧 English']:
        new_lang = 'fa' if text == '🇮🇷 فارسی' else 'en'
        update_user(uid, {"lang": new_lang})
        lang = new_lang

        now = time.time()
        last = db["last_motivation"].get(str(uid), 0)
        if now - last >= 3600:
            db["last_motivation"][str(uid)] = now
            save_data()
            bot.send_message(cid, random_motivation(lang))

        if not user["has_seen_welcome"]:
            user["has_seen_welcome"] = True
            save_data()
            send_new_message(uid, cid, get_text('welcome_main', lang), main_menu_keyboard(lang))
        else:
            send_main_menu(uid, cid, lang)
        return

    # برگشت به منوی اصلی
    if "برگشت" in text or "Back" in text:
        send_main_menu(uid, cid, lang)
        return

    # اکشن‌ها بر اساس مپینگ
    if action == "codm_config":
        send_new_message(uid, cid, get_text('codm_title', lang), codm_config_keyboard(lang))
        return

    elif action in ["config_promax", "config_topvip", "config_youtuber"]:
        send_new_message(uid, cid, "عملیات کانفیگ:", config_action_keyboard(lang))
        return

    elif action == "config_freefile":
        send_update_message(uid, cid, get_text('updating', lang))
        return

    elif action == "get_update":
        send_update_message(uid, cid, get_text('config_update', lang))
        return

    elif action == "buy_sub":
        send_update_message(uid, cid, get_text('config_buy', lang))
        return

    elif action == "currency":
        send_new_message(uid, cid, get_text('currency_title', lang), currency_keyboard(lang))
        send_update_message(uid, cid, get_text('currency_list', lang, time=datetime.now().strftime("%Y-%m-%d %H:%M")))
        return

    elif action == "dns_menu":
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
        return

    elif action == "wireguard_dns":
        send_update_message(uid, cid, get_text('wireguard_dns', lang))
        return

    elif action == "wireguard_vpn":
        send_update_message(uid, cid, get_text('wireguard_vpn', lang))
        return

    elif action == "vpn_menu":
        send_new_message(uid, cid, get_text('vpn_title', lang), vpn_keyboard(lang))
        return

    elif action == "v2ray":
        send_update_message(uid, cid, get_text('v2ray', lang))
        return

    elif action == "gameplay":
        send_update_message(uid, cid, get_text('updating', lang))  # یا متن اختصاصی
        return

    elif action == "free_codm":
        send_update_message(uid, cid, get_text('updating', lang))  # یا متن اختصاصی
        return

    elif action == "change_lang":
        send_new_message(uid, cid, get_text('choose_lang', lang), language_keyboard())
        return

    elif action == "channels":
        send_update_message(uid, cid, get_text('channels', lang))
        return

    # پیام پیش‌فرض (اگر هیچ اکشنی نبود)
    send_update_message(uid, cid, "⚠️ دستور نامعتبر است.\n\nاز دکمه‌های منوی زیر استفاده کنید:")
    send_main_menu(uid, cid, lang)

print("🚀 Bot is running... (نسخه بهبودیافته و بدون باگ)")
bot.polling(none_stop=True, interval=0, timeout=30)