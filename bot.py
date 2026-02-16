import telebot
import os
import random
import json
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')
bot = telebot.TeleBot(TOKEN)

CH1 = 'Karbawzi1File'
CH2 = 'Karbawzi1Trust'
ADMIN = '@Karbawzi1PV'
BOT = 'KarbawziUPDbot'

def stylish(t):
    m = str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        '𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇'
    )
    return t.translate(m)

MOT_FA = [
    "هیچ چیز تصادفی نیست، فقط هنوز دلیلش رو پیدا نکردی.",
    "تاریکی فقط نبود نور نیست، بلکه انتظار نوره.",
]
MOT_EN = [
    "Nothing is random, you just haven't found the reason yet.",
    "Darkness isn't the absence of light, it's the waiting for it.",
]

def motiv(lang):
    return random.choice(MOT_FA if lang == 'fa' else MOT_EN)

DATA = 'bot.json'

def load():
    try:
        with open(DATA, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": {}, "dns_free": {}, "motiv": {}}

db = load()

def save():
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def u(uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {
            "lang": "fa",
            "ref": f"r{uid}",
            "by": None,
            "invited": [],
            "claimed": {k: False for k in ["free", "artery", "vivan", "youtuber", "freefile", "codm"]},
            "last_msg": None,
            "welcome_done": False,
            "menu": "home"
        }
        save()
    return db["users"][uid]

def uu(uid, d):
    u(uid).update(d)
    save()

def joined(uid):
    try:
        for c in [CH1, CH2]:
            if bot.get_chat_member(f'@{c}', uid).status not in ['member','admin','creator']:
                return False
        return True
    except:
        return False

def count_inv(uid):
    return sum(1 for i in u(uid)["invited"] if joined(int(i)))

def add_inv(fr, to):
    fr, to = str(fr), str(to)
    if fr == to: return
    if to not in u(fr)["invited"]:
        u(fr)["invited"].append(to)
        save()

# ارسال بدون حذف
def send(cid, txt, kb=None):
    msg = bot.send_message(cid, txt, reply_markup=kb, parse_mode='Markdown')
    u(cid)["last_msg"] = msg.message_id
    save()
    return msg

def edit_panel(uid, cid, lang):
    user = u(uid)
    txt = "✨ به مرکز کنترل خوش آمدی!" if lang == 'fa' else stylish("✨ Welcome to Control Center!")
    
    last = user.get("last_msg")
    if last:
        try:
            bot.edit_message_text(txt, cid, last, reply_markup=home_kb(lang), parse_mode='Markdown')
            return
        except:
            pass
    
    send(cid, txt, home_kb(lang))

# کیبوردها
def home_kb(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    items = [
        ("🎮 Codm Config", "💱 Currency"),
        ("🎬 Gameplay", "🌐 DNS & WG"),
        ("🔒 VPN", "🆓 Free CODM"),
        ("🌍 Language", "📢 Channels")
    ] if lang == 'fa' else [
        (stylish("🎮 Codm Config"), stylish("💱 Currency")),
        (stylish("🎬 Gameplay"), stylish("🌐 DNS & WG")),
        (stylish("🔒 VPN"), stylish("🆓 Free CODM")),
        (stylish("🌍 Language"), stylish("📢 Channels"))
    ]
    for a, b in items:
        m.add(KeyboardButton(a), KeyboardButton(b))
    return m

def codm_kb(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    items = ["🚀 ProMax", "👑 TopVIP", "📺 YouTuber", "🆓 FreeFile"] if lang == 'fa' else [stylish(x) for x in ["🚀 ProMax", "👑 TopVIP", "📺 YouTuber", "🆓 FreeFile"]]
    m.add(*[KeyboardButton(i) for i in items])
    m.add(KeyboardButton("🔙 بازگشت" if lang == 'fa' else stylish("🔙 Back")))
    return m

def action_kb(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    items = ["📥 Update", "💰 Buy"] if lang == 'en' else ["📥 دریافت آپدیت", "💰 خرید اشتراک"]
    m.add(*[KeyboardButton(i) for i in items])
    m.add(KeyboardButton("🔙 بازگشت" if lang == 'fa' else stylish("🔙 Back")))
    return m

def dns_kb(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    items = ["🇮🇷 Irancell", "🇮🇷 MCI", "🇮🇷 Mokhaberat", "🇮🇷 Shatel", "🌍 Public", "🆓 Test", "🔧 WG-DNS", "🔧 WG-VPN"] if lang == 'en' else ["📶 ایرانسل", "📶 همراه اول", "📶 مخابرات", "📶 شاتل", "🌍 عمومی", "🆓 تست", "🔧 WG DNS", "🔧 WG VPN"]
    m.add(*[KeyboardButton(i) for i in items])
    m.add(KeyboardButton("🔙 بازگشت" if lang == 'fa' else stylish("🔙 Back")))
    return m

def vpn_kb(lang):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    items = ["WireGuard", "V2Ray"] if lang == 'en' else ["WireGuard", "V2Ray"]
    m.add(*[KeyboardButton(i) for i in items])
    m.add(KeyboardButton("🔙 بازگشت" if lang == 'fa' else stylish("🔙 Back")))
    return m

def lang_kb():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton("🇮🇷 فارسی"), KeyboardButton("🇬🇧 English"))
    m.add(KeyboardButton("🔙 بازگشت"))
    return m

# handlerها
@bot.message_handler(commands=['start'])
def start(m):
    uid = str(m.from_user.id)
    cid = m.chat.id
    user = u(uid)

    if len(m.text.split()) > 1 and m.text.split()[1].startswith('r'):
        inv = m.text.split()[1][1:]
        if inv != uid:
            add_inv(inv, uid)

    if not user["welcome_done"]:
        msg_send(cid, "به دنیای متفاوت خوش آمدی...\nزبان انتخاب کن", lang_kb())
    else:
        edit_panel(uid, cid, user["lang"])

@bot.message_handler(func=lambda m: True)
def handle(m):
    uid = str(m.from_user.id)
    cid = m.chat.id
    txt = m.text.strip()
    user = u(uid)
    lang = user["lang"]
    t = txt.lower()

    if "برگشت" in txt or "back" in t:
        edit_panel(uid, cid, lang)
        return

    if txt in ["🇮🇷 فارسی", "🇬🇧 English"]:
        nl = "fa" if txt == "🇮🇷 فارسی" else "en"
        user_update(uid, {"lang": nl})
        lang = nl

        now = time.time()
        last = db["motiv"].get(uid, 0)
        if now - last > 3600:
            db["motiv"][uid] = now
            save()
            bot.send_message(cid, motiv(lang))

        if not user["welcome_done"]:
            user_update(uid, {"welcome_done": True})
            msg_send(cid, "✨ خوش اومدی به مرکز!", home_kb(lang))
        else:
            edit_panel(uid, cid, lang)
        return

    # Codm Config
    if "codm" in t or "کالاف" in t or "config" in t:
        msg_send(cid, "انتخاب کن:", codm_kb(lang))
        return

    # زیرمنو Codm
    if any(w in t for w in ["promax", "topvip", "youtuber", "freefile", "پرو", "تاپ", "یوتیوب", "فری"]):
        msg_send(cid, "عملیات:", action_kb(lang))
        return

    # آپدیت / خرید
    if "آپدیت" in txt or "update" in t:
        msg_send(cid, "در حال آماده‌سازی نسخه جدید...")
        return
    if "خرید" in txt or "buy" in t:
        msg_send(cid, f"برای خرید پیام بده: {ADMIN}")
        return

    # DNS + Wireguard
    if "dns" in t or "دی ان اس" in t or "wireguard" in t:
        msg_send(cid, "بخش DNS و Wireguard", dns_kb(lang))
        return

    # VPN
    if "vpn" in t or "وی پی ان" in t:
        msg_send(cid, "بخش VPN", vpn_kb(lang))
        return

    # ارز
    if "ارز" in t or "currency" in t:
        msg_send(cid, "نرخ ارزها", currency_kb(lang))
        msg_send(cid, "در حال بارگذاری...")
        return

    # زبان
    if "زبان" in txt or "language" in t:
        msg_send(cid, "انتخاب زبان", lang_kb())
        return

    # کانال‌ها
    if "کانال" in txt or "channel" in t:
        msg_send(cid, f"کانال‌ها:\n@{CH1}\n@{CH2}")
        return

    msg_send(cid, "چیزی که گفتی رو پیدا نکردم...\nاز دکمه‌ها بزن لطفاً.")

print("Core online.")
bot.polling(none_stop=True, interval=0, timeout=30)