import telebot
import os
import random
import json
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

# Token from environment variable for Railway/GitHub
TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')
bot = telebot.TeleBot(TOKEN)

# Constants
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
    "「عمیق‌ترین چاه‌ها، خاموش‌ترین آب‌ها را دارند.» — ضرب‌المثل آلمانی",
    "「ستاره‌ها را نمی‌بینیم مگر اینکه شب شود.» — مثل هندی",
    "「کوه‌ها را جابه‌جا نمی‌کنیم، راهی دورشان پیدا می‌کنیم.» — فریدریش نیچه",
    "「بعضی کتاب‌ها را باید چشید، بعضی را بلعید، و بعضی را جوید و هضم کرد.» — فرانسیس بیکن",
]
MOTIVATION_EN = [
    "💭 \"We are what we repeatedly do. Excellence, then, is not an act, but a habit.\" — Aristotle",
    "💭 \"The cave you fear to enter holds the treasure you seek.\" — Joseph Campbell",
    "💭 \"No tree, it is said, can grow to heaven unless its roots reach down to hell.\" — Carl Jung",
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
            "claimed": {"free_account": False, "artery": False, "vivan": False, "youtuber": False, "freefile": False, "free_codm": False},
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
        return s1 in ['member', 'administrator', 'creator'] and s2 in ['member', 'administrator', 'creator']
    except:
        return False

def count_successful_referrals(uid):
    uid = str(uid)
    c = 0
    for ref in db["users"][uid].get("referrals_list", []):
        if is_member(int(ref)):
            c += 1
    return c

def add_referral(rid, nid):
    rid, nid = str(rid), str(nid)
    if rid == nid:
        return
    if nid not in db["users"][rid].get("referrals_list", []):
        db["users"][rid]["referrals_list"].append(nid)
        save_data()

def delete_previous_message(uid, cid):
    try:
        last_msg = db["users"].get(str(uid), {}).get("last_msg")
        if last_msg:
            bot.delete_message(cid, last_msg)
    except:
        pass

def delete_update_message(uid, cid):
    try:
        update_msg_id = db["users"].get(str(uid), {}).get("update_msg_id")
        if update_msg_id:
            bot.delete_message(cid, update_msg_id)
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
    return msg

def send_update_message(uid, cid, text):
    delete_update_message(uid, cid)
    msg = bot.send_message(cid, text, parse_mode='Markdown')
    db["users"][str(uid)]["update_msg_id"] = msg.message_id
    save_data()
    return msg

def send_main_menu(uid, cid, lang):
    delete_update_message(uid, cid)
    user = get_user(uid)
    main_text = get_text('welcome_main', lang)

    if user.get("last_msg"):
        try:
            bot.edit_message_text(
                chat_id=cid,
                message_id=user["last_msg"],
                text=main_text,
                reply_markup=main_menu_keyboard(lang),
                parse_mode='Markdown'
            )
            return
        except:
            pass  # Fallback to new message if edit fails

    msg = bot.send_message(cid, main_text, reply_markup=main_menu_keyboard(lang), parse_mode='Markdown')
    user["last_msg"] = msg.message_id
    save_data()

def get_text(key, lang, **kwargs):
    texts = {
        'promotion': {
            'fa': "✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌\n\n🔥 Karbawzi UPD\nفراتر از یه بات ساده...\nاینجا فقط بات نیست، یک گوشه از هزاران رد پای من هست.\n\n👤 ادمین: @Karbawzi1PV\n📢 کانال اول: @Karbawzi1File\n🔒 کانال دوم: @Karbawzi1Trust\n\nما موندگاریم، چون متفاوتیم.",
            'en': fancy_text("✨ KARBAWZI PREMIUM\n\n🔥 Karbawzi UPD\nBeyond a simple bot...\nThis is not just a bot, it's a corner of thousands of my footprints.\n\n👤 Admin: @Karbawzi1PV\n📢 Channel 1: @Karbawzi1File\n🔒 Channel 2: @Karbawzi1Trust\n\nWe endure because we are unique.")
        },
        'choose_lang': {
            'fa': '🌍 زبان خود را انتخاب کنید:',
            'en': fancy_text('🌍 Select Your Language:')
        },
        'welcome_main': {
            'fa': '✨ به پنل اصلی خوش آمدید! 🚀\n\nلطفاً گزینه مورد نظر را انتخاب کنید.',
            'en': fancy_text('✨ Welcome to the Main Panel! 🚀\n\nPlease select an option below.')
        },
        'updating_ui': {
            'fa': '🔄 در حال بروزرسانی سورس برای بهبود رابط کاربری...\n\n⏳ لطفاً صبر کنید. به زودی آماده خواهد شد! ✨',
            'en': fancy_text('🔄 Updating source for enhanced UI...\n\n⏳ Please wait. It will be ready soon! ✨')
        },
        'dns_free_active': {
            'fa': '✅ تست رایگان DNS فعال شد!\n\n🛡️ Primary: `78.157.53.52`\n🛡️ Secondary: `78.157.53.219`\n\n⏳ {time} باقی‌مانده\n\n💡 برای استفاده، DNS دستگاه خود را تغییر دهید.',
            'en': fancy_text('✅ Free DNS Test Activated!\n\n🛡️ Primary: `78.157.53.52`\n🛡️ Secondary: `78.157.53.219`\n\n⏳ {time} remaining\n\n💡 Change your device DNS to use.')
        },
        'dns_free_req': {
            'fa': '❌ برای فعال‌سازی تست رایگان، حداقل ۲ دعوت موفق (عضویت در کانال‌ها) نیاز است.\n\n📊 وضعیت فعلی: {cnt}/2\n\n🔗 لینک معرفی خود را به اشتراک بگذارید!',
            'en': fancy_text('❌ To activate free test, you need at least 2 successful referrals (channel joins).\n\n📊 Current status: {cnt}/2\n\n🔗 Share your referral link!')
        },
        'dns_public_note': {
            'fa': '🌍 Public Free DNS Servers\n\nانتخاب کنید و DNS دستگاه را تنظیم کنید:',
            'en': fancy_text('🌍 Public Free DNS Servers\n\nSelect and configure your device DNS:')
        },
        'referral_link': {
            'fa': '🔗 **لینک اختصاصی معرفی شما**\n\n🌟 https://t.me/{bot}?start={ref}\n\n📢 بات ما: @KarbawziUPDbot\n\n💎 با هر دعوت موفق، به جوایز نزدیک‌تر شوید!\n\n👥 دوستان خود را دعوت کنید و امتیاز جمع‌آوری کنید. 🚀',
            'en': fancy_text('🔗 **Your Exclusive Referral Link**\n\n🌟 https://t.me/{bot}?start={ref}\n\n📢 Our Bot: @KarbawziUPDbot\n\n💎 Get closer to rewards with each successful invite!\n\n👥 Invite friends and earn points. 🚀')
        },
        'account_credentials': {
            'fa': '📋 **اطلاعات اکانت تست**\n\n📧 ایمیل: `test@gmail.com`\n🔑 پسورد: `test.`\n\n⚠️ فقط برای تست - پس از ۲۴ ساعت منقضی می‌شود.',
            'en': fancy_text('📋 **Test Account Credentials**\n\n📧 Email: `test@gmail.com`\n🔑 Password: `test.`\n\n⚠️ For testing only - expires in 24 hours.')
        },
        'codm_title': {'fa': '🎮 Codm Config', 'en': fancy_text('🎮 Codm Config')},
        'youtuber_title': {'fa': '📺 Youtuber Configs', 'en': fancy_text('📺 Youtuber Configs')},
        'free_codm_title': {'fa': '🆓 Free CODM', 'en': fancy_text('🆓 Free CODM')},
        'currency_title': {'fa': '💱 قیمت ارز', 'en': fancy_text('💱 Currency Prices')},
        'gameplay_title': {'fa': '🎬 گیم پلی', 'en': fancy_text('🎬 Gameplay')},
        'dns_title': {'fa': '🌐 DNS Section', 'en': fancy_text('🌐 DNS Section')},
        'wireguard_title': {'fa': '🔐 Wireguard Section', 'en': fancy_text('🔐 Wireguard Section')},
        'usd_info': {
            'en': fancy_text('💵 **USD (United States Dollar) Detailed Information**\n\nThe US Dollar (USD) is the world\'s primary reserve currency and the most traded currency globally. As of the latest market data:\n\n📈 **Current Rate:** 1 USD = 42,000 IRR (approximate, subject to fluctuation)\n📊 **24-Hour Change:** +0.5%\n📉 **52-Week Range:** 38,000 - 45,000 IRR\n\n🔍 **Key Factors Influencing USD:**\n- Federal Reserve interest rate decisions\n- US economic indicators (GDP, employment reports)\n- Geopolitical events and global trade balances\n- Inflation trends and commodity prices (oil, gold)\n\n💡 **Trading Tips:** Monitor the US Non-Farm Payrolls report for volatility. Use stop-loss orders in forex trading to manage risks.\n\nFor real-time updates, consider integrating with financial APIs like Alpha Vantage or Yahoo Finance.\n\n🔄 Last updated: {time}')
        },
        'eur_info': {
            'en': fancy_text('€ **EUR (Euro) Detailed Information**\n\nThe Euro (EUR) is the official currency of the Eurozone, used by 20 EU countries. Current insights:\n\n📈 **Current Rate:** 1 EUR = 45,500 IRR\n📊 **24-Hour Change:** -0.2%\n📉 **52-Week Range:** 41,000 - 48,000 IRR\n\n🔍 **Key Factors Influencing EUR:**\n- European Central Bank (ECB) monetary policy\n- Eurozone economic growth and inflation data\n- Brexit aftermath and EU-US trade relations\n- Energy prices and global supply chain disruptions\n\n💡 **Investment Advice:** EUR/USD pair is popular for carry trades. Watch ECB meetings for rate hike signals.\n\nStay informed with sources like Bloomberg or Reuters for in-depth analysis.\n\n🔄 Last updated: {time}')
        },
        'btc_info': {
            'en': fancy_text('₿ **BTC (Bitcoin) Detailed Information**\n\nBitcoin (BTC), the pioneer cryptocurrency, continues to dominate the crypto market with its decentralized nature.\n\n📈 **Current Price:** 1 BTC = 1,800,000,000 IRR (\~$42,000 USD)\n📊 **24-Hour Change:** +3.1%\n📉 **52-Week Range:** 1,200,000,000 - 2,500,000,000 IRR\n\n🔍 **Key Factors Influencing BTC:**\n- Institutional adoption (ETFs, corporate treasuries)\n- Regulatory developments (SEC approvals, global bans)\n- Halving events and mining difficulty adjustments\n- Market sentiment from influencers and whale movements\n- Correlation with traditional assets during risk-off periods\n\n💡 **Trading Strategies:** Dollar-cost averaging (DCA) for long-term holding. Use technical analysis like RSI and moving averages for entries.\n\nResources: CoinMarketCap, TradingView for charts, and Blockchain.com for on-chain metrics.\n\n⚠️ **Risk Warning:** High volatility; invest only what you can afford to lose.\n\n🔄 Last updated: {time}')
        },
        'req_msg': {
            'fa': '❌ نیاز به {need} دعوت موفق دیگر! 📈\n\n💡 هر دعوت موفق شما را به جوایز نزدیک‌تر می‌کند. 🔗 لینک معرفی را به اشتراک بگذارید.',
            'en': fancy_text('❌ Need {need} more successful invites! 📈\n\n💡 Each successful invite brings you closer to rewards. 🔗 Share your referral link.')
        },
        'already_claimed': {
            'fa': '⚠️ قبلاً دریافت کردید! 🔄\n\n💡 برای جوایز بیشتر، دعوت‌های خود را افزایش دهید.',
            'en': fancy_text('⚠️ Already claimed! 🔄\n\n💡 Increase your invites for more rewards.')
        },
        'join_channels': {
            'fa': '❌ ابتدا عضو کانال‌ها شوید! 👆\n\n📢 @{ch1}\n🔒 @{ch2}',
            'en': fancy_text('❌ Join channels first! 👆\n\n📢 @{ch1}\n🔒 @{ch2}')
        }
    }
    return texts.get(key, {}).get(lang, '').format(**kwargs)

def language_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("🇮🇷 فارسی"), KeyboardButton("🇬🇧 English"))
    return markup

def main_menu_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == 'fa':
        buttons = [
            KeyboardButton("🎮 Codm Config"),
            KeyboardButton("💱 قیمت ارز"),
            KeyboardButton("🎬 گیم پلی"),
            KeyboardButton("🌐 DNS"),
            KeyboardButton("🔐 وایرگارد"),
            KeyboardButton("🆓 کالاف دیوتی"),
            KeyboardButton("🌍 تغییر زبان"),
            KeyboardButton("📢 کانال‌ها")
        ]
    else:
        buttons = [
            KeyboardButton(fancy_text("🎮 Codm Config")),
            KeyboardButton(fancy_text("💱 Currency Prices")),
            KeyboardButton(fancy_text("🎬 Gameplay")),
            KeyboardButton(fancy_text("🌐 DNS")),
            KeyboardButton(fancy_text("🔐 Wireguard")),
            KeyboardButton(fancy_text("🆓 CODM")),
            KeyboardButton(fancy_text("🌍 Change Language")),
            KeyboardButton(fancy_text("📢 Channels"))
        ]
    markup.add(*buttons)
    return markup

def back_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def codm_config_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == 'fa':
        buttons = [
            KeyboardButton("🚀 ProMax"),
            KeyboardButton("👑 TopVIP"),
            KeyboardButton("📺 Youtuber"),
            KeyboardButton("🆓 FreeFile"),
            KeyboardButton("🔙 برگشت به منوی اصلی")
        ]
    else:
        buttons = [
            KeyboardButton(fancy_text("🚀 ProMax")),
            KeyboardButton(fancy_text("👑 TopVIP")),
            KeyboardButton(fancy_text("📺 Youtuber")),
            KeyboardButton(fancy_text("🆓 FreeFile")),
            KeyboardButton(fancy_text("🔙 Back to Main Menu"))
        ]
    markup.add(*buttons)
    return markup

def currency_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        KeyboardButton(fancy_text("💵 USD")),
        KeyboardButton(fancy_text("€ EUR")),
        KeyboardButton(fancy_text("₿ BTC")),
        KeyboardButton(fancy_text("🔙 Back to Main Menu"))
    ]
    markup.add(*buttons)
    return markup

def gameplay_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for i in range(1, 31):
        btn_text = f"🎬 Gameplay {i}" if lang == 'en' else f"🎬 گیم پلی {i}"
        buttons.append(KeyboardButton(btn_text if lang == 'en' else btn_text))
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i+1])
        else:
            markup.row(buttons[i])
    markup.add(KeyboardButton(fancy_text("🔙 Back to Main Menu") if lang == 'en' else "🔙 برگشت به منوی اصلی"))
    return markup

def dns_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == 'fa':
        buttons = [
            KeyboardButton("📶 ایرانسل"),
            KeyboardButton("📶 همراه اول"),
            KeyboardButton("📶 مخابرات"),
            KeyboardButton("📶 شاتل"),
            KeyboardButton("🌍 Public DNS"),
            KeyboardButton("🧪 Free Test"),
            KeyboardButton("🔙 برگشت به منوی اصلی")
        ]
    else:
        buttons = [
            KeyboardButton(fancy_text("📶 Irancell")),
            KeyboardButton(fancy_text("📶 MCI")),
            KeyboardButton(fancy_text("📶 Mokhaberat")),
            KeyboardButton(fancy_text("📶 Shatel")),
            KeyboardButton(fancy_text("🌍 Public DNS")),
            KeyboardButton(fancy_text("🧪 Free Test")),
            KeyboardButton(fancy_text("🔙 Back to Main Menu"))
        ]
    markup.add(*buttons)
    return markup

def wireguard_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == 'fa':
        buttons = [
            KeyboardButton("🔐 VPN"),
            KeyboardButton("🌐 DNS"),
            KeyboardButton("🔙 برگشت به منوی اصلی")
        ]
    else:
        buttons = [
            KeyboardButton(fancy_text("🔐 VPN")),
            KeyboardButton(fancy_text("🌐 DNS")),
            KeyboardButton(fancy_text("🔙 Back to Main Menu"))
        ]
    markup.add(*buttons)
    return markup

def codm_keyboard(lang, uid):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    is_mem = is_member(uid)
    cnt = count_successful_referrals(uid)
    if lang == 'fa':
        free_text = f"🎮 اکانت رایگان {'✅' if is_mem else '❌'} | {cnt}/5"
        artery_text = f"🔥 Artery {'✅' if is_mem else '❌'} | {cnt}/10"
        vivan_text = f"✨ Vivan Harris {'✅' if is_mem else '❌'} | {cnt}/15"
        buttons = [
            KeyboardButton(free_text),
            KeyboardButton(artery_text),
            KeyboardButton(vivan_text),
            KeyboardButton("📋 لیست کمبو"),
            KeyboardButton("🔗 لینک معرفی"),
            KeyboardButton("🔙 برگشت به منوی اصلی")
        ]
    else:
        free_text = fancy_text(f"🎮 Free Account {'✅' if is_mem else '❌'} | {cnt}/5")
        artery_text = fancy_text(f"🔥 Artery {'✅' if is_mem else '❌'} | {cnt}/10")
        vivan_text = fancy_text(f"✨ Vivan Harris {'✅' if is_mem else '❌'} | {cnt}/15")
        buttons = [
            KeyboardButton(free_text),
            KeyboardButton(artery_text),
            KeyboardButton(vivan_text),
            KeyboardButton(fancy_text("📋 Combo List")),
            KeyboardButton(fancy_text("🔗 Referral Link")),
            KeyboardButton(fancy_text("🔙 Back to Main Menu"))
        ]
    markup.add(*buttons)
    return markup

# DNS Public List
dns_public_list = {
    'google': {'en': '🛡️ Google DNS', 'ips': 'Primary: 8.8.8.8\nSecondary: 8.8.4.4'},
    'cloudflare': {'en': '☁️ Cloudflare', 'ips': 'Primary: 1.1.1.1\nSecondary: 1.0.0.1'},
    'opendns': {'en': '🔓 OpenDNS', 'ips': 'Primary: 208.67.222.222\nSecondary: 208.67.220.220'},
    'quad9': {'en': '🔢 Quad9', 'ips': 'Primary: 9.9.9.9\nSecondary: 149.112.112.112'},
    'cleanbrowsing': {'en': '🧹 CleanBrowsing', 'ips': 'Primary: 185.228.168.9\nSecondary: 185.228.169.9'},
    'adguard': {'en': '🚫 AdGuard', 'ips': 'Primary: 94.140.14.14\nSecondary: 94.140.15.15'},
    'nextdns': {'en': '🚀 NextDNS', 'ips': 'Primary: 45.90.28.0\nSecondary: 45.90.30.0 (Custom config required)'},
}

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    cid = m.chat.id
    args = m.text.split()
    
    if len(args) > 1 and args[1].startswith('ref'):
        try:
            rid = args[1][3:]
            if rid != str(uid):
                add_referral(rid, uid)
                get_user(uid)["referred_by"] = rid
                save_data()
        except:
            pass
    
    user = get_user(uid)
    
    # Do not delete /start message
    
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
    
    # Delete user message except /start
    if not m.text.startswith('/start'):
        try:
            bot.delete_message(cid, m.message_id)
        except:
            pass
    
    # Language selection
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
    
    # Back to main
    if text in ['🔙 برگشت به منوی اصلی', fancy_text("🔙 Back to Main Menu")]:
        update_user(uid, {"current_menu": "main"})
        send_main_menu(uid, cid, lang)
        return
    
    # Channels
    if text in ['📢 کانال‌ها', fancy_text("📢 Channels")]:
        bot.send_message(cid, f"📢 @{CHANNEL1}\n🔒 @{CHANNEL2}\n\n✅ برای دسترسی به جوایز، عضو شوید!")
        send_main_menu(uid, cid, lang)
        return
    
    # Change language
    if text in ['🌍 تغییر زبان', fancy_text("🌍 Change Language")]:
        send_new_message(uid, cid, get_text('choose_lang', lang), language_keyboard())
        return
    
    # Codm Config
    if text in ['🎮 Codm Config', fancy_text("🎮 Codm Config")]:
        send_new_message(uid, cid, get_text('codm_title', lang), codm_config_keyboard(lang))
        return
    
    # Codm Config submenus
    codm_keys = ['promax', 'topvip', 'youtuber', 'freefile']
    for k in codm_keys:
        fa_text = {'promax': '🚀 ProMax', 'topvip': '👑 TopVIP', 'youtuber': '📺 Youtuber', 'freefile': '🆓 FreeFile'}[k]
        en_text = fancy_text(fa_text)
        if text == fa_text or text == en_text:
            send_update_message(uid, cid, get_text('updating_ui', lang))
            send_new_message(uid, cid, get_text('codm_title', lang), codm_config_keyboard(lang))
            return
    
    # Currency Prices
    if text in ['💱 قیمت ارز', fancy_text("💱 Currency Prices")]:
        send_new_message(uid, cid, get_text('currency_title', lang), currency_keyboard(lang))
        return
    
    # Currency details (always English)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if fancy_text("💵 USD") in text:
        info = get_text('usd_info', 'en', time=now)
        send_update_message(uid, cid, info)
        send_new_message(uid, cid, get_text('currency_title', lang), currency_keyboard(lang))
        return
    if fancy_text("€ EUR") in text:
        info = get_text('eur_info', 'en', time=now)
        send_update_message(uid, cid, info)
        send_new_message(uid, cid, get_text('currency_title', lang), currency_keyboard(lang))
        return
    if fancy_text("₿ BTC") in text:
        info = get_text('btc_info', 'en', time=now)
        send_update_message(uid, cid, info)
        send_new_message(uid, cid, get_text('currency_title', lang), currency_keyboard(lang))
        return
    
    # Gameplay
    if text in ['🎬 گیم پلی', fancy_text("🎬 Gameplay")]:
        send_new_message(uid, cid, get_text('gameplay_title', lang), gameplay_keyboard(lang))
        return
    
    if text.startswith('🎬 گیم پلی') or text.startswith(fancy_text('🎬 Gameplay')):
        send_update_message(uid, cid, get_text('updating_ui', lang))
        send_new_message(uid, cid, get_text('gameplay_title', lang), gameplay_keyboard(lang))
        return
    
    # DNS
    if text in ['🌐 DNS', fancy_text("🌐 DNS")]:
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
        return
    
    # DNS sub (Iran providers to update)
    if any(provider in text for provider in ['ایرانسل', 'همراه اول', 'مخابرات', 'شاتل', fancy_text("Irancell"), fancy_text("MCI"), fancy_text("Mokhaberat"), fancy_text("Shatel")]):
        send_update_message(uid, cid, get_text('updating_ui', lang))
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
        return
    
    # Public DNS
    if text in ['🌍 Public DNS', fancy_text("🌍 Public DNS")]:
        txt = get_text('dns_public_note', lang) + "\n\n"
        for k, v in dns_public_list.items():
            txt += f"• {v['en']}:\n  {v['ips']}\n\n"
        send_update_message(uid, cid, txt)
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
        return
    
    # Free Test DNS
    if text in ['🧪 Free Test', fancy_text("🧪 Free Test")]:
        cnt = count_successful_referrals(uid)
        if cnt < 2:
            req_msg = get_text('dns_free_req', lang, cnt=cnt)
            send_update_message(uid, cid, req_msg)
            send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
            return
        
        now = time.time()
        uid_str = str(uid)
        if uid_str in db["dns_free"]:
            rem = 6*3600 - (now - db["dns_free"][uid_str])
            if rem > 0:
                h = int(rem//3600)
                m = int((rem%3600)//60)
                ts = f"{h}ساعت {m}دقیقه" if lang == 'fa' else f"{h}h {m}m"
                active_msg = get_text('dns_free_active', lang, time=ts)
                send_update_message(uid, cid, active_msg)
                send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
                return
            else:
                del db["dns_free"][uid_str]
                save_data()
        
        db["dns_free"][uid_str] = now
        save_data()
        ts = "۶ ساعت ۰ دقیقه" if lang == 'fa' else "6h 0m"
        active_msg = get_text('dns_free_active', lang, time=ts)
        send_update_message(uid, cid, active_msg)
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
        return
    
    # Wireguard
    if text in ['🔐 وایرگارد', fancy_text("🔐 Wireguard")]:
        send_new_message(uid, cid, get_text('wireguard_title', lang), wireguard_keyboard(lang))
        return
    
    if text in ['🔐 VPN', fancy_text("🔐 VPN")]:
        send_update_message(uid, cid, get_text('updating_ui', lang))
        send_new_message(uid, cid, get_text('wireguard_title', lang), wireguard_keyboard(lang))
        return
    
    # CODM
    if text in ['🆓 کالاف دیوتی', fancy_text("🆓 CODM")]:
        update_user(uid, {"current_menu": "codm"})
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
        return
    
    # CODM claims
    def handle_claim(text_start, claimed_key, req_cnt):
        if not is_member(uid):
            join_msg = get_text('join_channels', lang, ch1=CHANNEL1, ch2=CHANNEL2)
            send_update_message(uid, cid, join_msg)
            send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
            return
        
        cnt = count_successful_referrals(uid)
        if cnt >= req_cnt:
            if not user["claimed"][claimed_key]:
                cred_msg = get_text('account_credentials', lang)
                send_update_message(uid, cid, cred_msg)
                db["users"][str(uid)]["claimed"][claimed_key] = True
                save_data()
            else:
                already_msg = get_text('already_claimed', lang)
                send_update_message(uid, cid, already_msg)
        else:
            need = req_cnt - cnt
            req_msg = get_text('req_msg', lang, need=need)
            send_update_message(uid, cid, req_msg)
        
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
    
    if text.startswith('🎮 اکانت رایگان') or text.startswith(fancy_text('🎮 Free Account')):
        handle_claim(text, "free_account", 5)
        return
    if text.startswith('🔥 Artery') or text.startswith(fancy_text('🔥 Artery')):
        handle_claim(text, "artery", 10)
        return
    if text.startswith('✨ Vivan Harris') or text.startswith(fancy_text('✨ Vivan Harris')):
        handle_claim(text, "vivan", 15)
        return
    
    # Combo List
    if text in ['📋 لیست کمبو', fancy_text("📋 Combo List")]:
        if not is_member(uid):
            join_msg = get_text('join_channels', lang, ch1=CHANNEL1, ch2=CHANNEL2)
            send_update_message(uid, cid, join_msg)
        else:
            combo_msg = f"👤 تماس با ادمین: {ADMIN_ID}\n\n📝 لیست کمبو به زودی در کانال‌ها!"
            send_update_message(uid, cid, combo_msg)
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
        return
    
    # Referral Link
    if text in ['🔗 لینک معرفی', fancy_text("🔗 Referral Link")]:
        ref_msg = get_text('referral_link', lang, bot=BOT_USERNAME, ref=user["ref_code"])
        send_update_message(uid, cid, ref_msg)
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
        return

print("🚀 Karbawzi UPD Bot is running with enhanced REPLY KEYBOARD... ✨")
bot.polling(none_stop=True, interval=0, timeout=30)