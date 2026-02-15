import telebot, os, random, json, time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

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
    return random.choice(MOTIVATION_FA if lang=='fa' else MOTIVATION_EN)

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
            "update_msg_id": None,
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
    lst = db["users"][rid].setdefault("referrals_list", [])
    if nid not in lst:
        lst.append(nid)
        save_data()

def delete_previous_message(uid, cid):
    try:
        last = db["users"][str(uid)].get("last_msg")
        if last:
            bot.delete_message(cid, last)
    except:
        pass

def delete_update_message(uid, cid):
    try:
        up = db["users"][str(uid)].get("update_msg_id")
        if up:
            bot.delete_message(cid, up)
            db["users"][str(uid)]["update_msg_id"] = None
            save_data()
    except:
        pass

def send_new_message(uid, cid, text, reply_markup=None):
    delete_previous_message(uid, cid)
    delete_update_message(uid, cid)
    msg = bot.send_message(cid, text, reply_markup=reply_markup, parse_mode='Markdown')
    db["users"][str(uid)]["last_msg"] = msg.message_id
    save_data()

def send_update_message(uid, cid, text):
    delete_update_message(uid, cid)
    msg = bot.send_message(cid, text, parse_mode='Markdown')
    db["users"][str(uid)]["update_msg_id"] = msg.message_id
    save_data()

def send_main_menu(uid, cid, lang):
    delete_update_message(uid, cid)
    txt = get_text('welcome_main', lang)
    user = get_user(uid)
    last = user.get("last_msg")
    if last:
        try:
            bot.edit_message_text(txt, cid, last, reply_markup=main_menu_keyboard(lang), parse_mode='Markdown')
            return
        except:
            pass
    msg = bot.send_message(cid, txt, reply_markup=main_menu_keyboard(lang), parse_mode='Markdown')
    user["last_msg"] = msg.message_id
    save_data()

# ────────────────────────────────────────────────
# متن‌ها (اینجا همه رو گذاشتم – اگر چیزی کم بود بگو اضافه کنم)

def get_text(key, lang, **kwargs):
    texts = {
        'promotion': {
            'fa': "✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌\n\n🔥 karbawzi UPD\nفراتر از یه بات ساده...\n\n👤 ادمین: @Karbawzi1PV\n📢 @Karbawzi1File\n🔒 @Karbawzi1Trust\n\nما موندگاریم، چون متفاوتیم.",
            'en': fancy_text("✨ KARBAWZI PREMIUM\n\n🔥 karbawzi UPD\nMore than a simple bot...\n\n👤 Admin: @Karbawzi1PV\n📢 @Karbawzi1File\n🔒 @Karbawzi1Trust\n\nWe stay, because we are different.")
        },
        'choose_lang': {
            'fa': '🌍 زبان خود را انتخاب کنید:',
            'en': fancy_text('🌍 Choose your language:')
        },
        'welcome_main': {
            'fa': '✨ به پنل اصلی خوش آمدید! 🚀\n\nلطفاً گزینه مورد نظر را انتخاب کنید.',
            'en': fancy_text('✨ Welcome to Main Panel! 🚀\n\nPlease choose an option.')
        },
        'updating_ui': {
            'fa': '🔄 در حال بروزرسانی سورس برای بهبود رابط کاربری...\n\n⏳ لطفاً صبر کنید.',
            'en': fancy_text('🔄 Updating source for better UI...\n\n⏳ Please wait.')
        },
        'dns_free_active': {
            'fa': '✅ تست رایگان فعال\n\nپرایمری: `78.157.53.52`\nثانویه: `78.157.53.219`\n\n⏳ {time} باقی‌مانده',
            'en': fancy_text('✅ Free test active\n\nPrimary: `78.157.53.52`\nSecondary: `78.157.53.219`\n\n⏳ {time} left')
        },
        'dns_free_req': {
            'fa': '❌ برای فعال‌سازی تست رایگان حداقل ۲ دعوت موفق نیاز است.\nوضعیت فعلی: {cnt}/2',
            'en': fancy_text('❌ Need at least 2 successful invites for free test.\nCurrent: {cnt}/2')
        },
        'referral_link': {
            'fa': '🔗 لینک معرفی شما:\n`https://t.me/{bot}?start={ref}`',
            'en': fancy_text('🔗 Your referral link:\n`https://t.me/{bot}?start={ref}`')
        },
        'account_credentials': {
            'fa': '📋 اکانت تست\n📧 `test@gmail.com`\n🔑 `test.`',
            'en': fancy_text('📋 Test account\n📧 `test@gmail.com`\n🔑 `test.`')
        },
        'codm_title': {'fa': '🎮 Codm Config', 'en': fancy_text('🎮 Codm Config')},
        'currency_title': {'fa': '💱 قیمت ارز', 'en': fancy_text('💱 Currency Prices')},
        'gameplay_title': {'fa': '🎬 گیم پلی', 'en': fancy_text('🎬 Gameplay')},
        'dns_title': {'fa': '🌐 DNS Section', 'en': fancy_text('🌐 DNS Section')},
        'wireguard_title': {'fa': '🔐 Wireguard Section', 'en': fancy_text('🔐 Wireguard Section')},
        'req_msg': {
            'fa': '❌ نیاز به {need} دعوت موفق دیگر!',
            'en': fancy_text('❌ Need {need} more successful invites!')
        },
        'already_claimed': {
            'fa': '⚠️ قبلاً دریافت کردید',
            'en': fancy_text('⚠️ Already claimed')
        },
        'join_channels': {
            'fa': '❌ ابتدا عضو کانال‌ها شوید!',
            'en': fancy_text('❌ Join channels first!')
        }
    }
    return texts.get(key, {}).get(lang, '').format(**kwargs)

# ────────────────────────────────────────────────
# کیبوردها

def language_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("🇮🇷 فارسی"), KeyboardButton("🇬🇧 English"))
    return markup

def main_menu_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == 'fa':
        btns = [
            "🎮 Codm Config", "💱 قیمت ارز", "🎬 گیم پلی",
            "🌐 DNS", "🔐 وایرگارد", "🆓 کالاف دیوتی",
            "🌍 تغییر زبان", "📢 کانال‌ها"
        ]
    else:
        btns = [fancy_text(b) for b in [
            "🎮 Codm Config", "💱 Currency Prices", "🎬 Gameplay",
            "🌐 DNS", "🔐 Wireguard", "🆓 CODM",
            "🌍 Change Language", "📢 Channels"
        ]]
    markup.add(*[KeyboardButton(b) for b in btns])
    return markup

def back_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    txt = "🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")
    markup.add(KeyboardButton(txt))
    return markup

# بقیه کیبوردها (dns, wireguard, codm config, currency, gameplay, codm) رو اگر خواستی اضافه کن – فعلاً ساده نگه داشتم تا تست کنی

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
    lang = user["lang"]

    try:
        bot.delete_message(cid, m.message_id)
    except:
        pass

    if text in ["🇮🇷 فارسی", "🇬🇧 English"]:
        new_lang = 'fa' if text == "🇮🇷 فارسی" else 'en'
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

    t = text.lower()

    if "برگشت" in text or "back to main" in t:
        update_user(uid, {"current_menu": "main"})
        send_main_menu(uid, cid, lang)
        return

    if "تغییر زبان" in text or "change language" in t:
        send_new_message(uid, cid, get_text('choose_lang', lang), language_keyboard())
        return

    if "codm config" in t or "کالاف" in text:
        update_user(uid, {"current_menu": "codm"})
        send_new_message(uid, cid, get_text('codm_title', lang), back_keyboard(lang))
        return

    if "قیمت ارز" in text or "currency" in t:
        send_new_message(uid, cid, get_text('currency_title', lang), back_keyboard(lang))
        return

    if "گیم پلی" in text or "gameplay" in t:
        send_new_message(uid, cid, get_text('gameplay_title', lang), back_keyboard(lang))
        return

    if "dns" in t:
        send_new_message(uid, cid, get_text('dns_title', lang), back_keyboard(lang))
        return

    if "وایرگارد" in text or "wireguard" in t:
        send_new_message(uid, cid, get_text('wireguard_title', lang), back_keyboard(lang))
        return

    send_update_message(uid, cid, "دستور شناخته نشد.\nاز دکمه‌های منو استفاده کنید.")

print("🚀 Bot is running...")
bot.polling(none_stop=True, interval=0, timeout=30)