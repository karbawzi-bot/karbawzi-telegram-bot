import telebot, os, random, json, time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')
bot = telebot.TeleBot(TOKEN)
CHANNEL1, CHANNEL2, ADMIN_ID, BOT_USERNAME = 'Karbawzi1File', 'Karbawzi1Trust', '@Karbawzi1PV', 'YourBotUsername'

def fancy_text(t):
    m={'A':'𝙰','B':'𝙱','C':'𝙲','D':'𝙳','E':'𝙴','F':'𝙵','G':'𝙶','H':'𝙷','I':'𝙸','J':'𝙹','K':'𝙺','L':'𝙻','M':'𝙼','N':'𝙽','O':'𝙾','P':'𝙿','Q':'𝚀','R':'𝚁','S':'𝚂','T':'𝚃','U':'𝚄','V':'𝚅','W':'𝚆','X':'𝚇','Y':'𝚈','Z':'𝚉','a':'𝚊','b':'𝚋','c':'𝚌','d':'𝚍','e':'𝚎','f':'𝚏','g':'𝚐','h':'𝚑','i':'𝚒','j':'𝚓','k':'𝚔','l':'𝚕','m':'𝚖','n':'𝚗','o':'𝚘','p':'𝚙','q':'𝚚','r':'𝚛','s':'𝚜','t':'𝚝','u':'𝚞','v':'𝚟','w':'𝚠','x':'𝚡','y':'𝚢','z':'𝚣'}
    return ''.join(m.get(c,c) for c in t)

MOTIVATION_FA = [
    "「انسان همان‌طور فکر می‌کند که زندگی می‌کند، نه همان‌طور که زندگی می‌کند فکر می‌کند。」 — ریلکه",
    "「عمیق‌ترین چاه‌ها، خاموش‌ترین آب‌ها را دارند。」 — ضرب‌المثل آلمانی",
    "「ستاره‌ها را نمی‌بینیم مگر اینکه شب شود。」 — مثل هندی",
    "「کوه‌ها را جابه‌جا نمی‌کنیم، راهی دورشان پیدا می‌کنیم。」 — فریدریش نیچه",
    "「بعضی کتاب‌ها را باید چشید، بعضی را بلعید، و بعضی را جوید و هضم کرد。」 — فرانسیس بیکن",
]
MOTIVATION_EN = [
    "💭 \"We are what we repeatedly do. Excellence, then, is not an act, but a habit.\" — Aristotle",
    "💭 \"The cave you fear to enter holds the treasure you seek.\" — Joseph Campbell",
    "💭 \"No tree, it is said, can grow to heaven unless its roots reach down to hell.\" — Carl Jung",
]

def random_motivation(lang):
    return random.choice(MOTIVATION_FA if lang=='fa' else MOTIVATION_EN)

DATA_FILE='bot_data.json'
def load_data():
    try:
        with open(DATA_FILE,'r',encoding='utf-8') as f: return json.load(f)
    except: return {"users":{},"dns_free":{},"last_motivation":{}}
db=load_data()
def save_data(): 
    with open(DATA_FILE,'w',encoding='utf-8') as f: json.dump(db,f,ensure_ascii=False,indent=2)

def get_user(uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"lang":"fa","ref_code":f"ref{uid}","referred_by":None,"referrals_list":[],"claimed":{"free_account":False,"artery":False,"vivan":False,"combo":False}, "last_msg": None, "current_menu": "main"}
        save_data()
    return db["users"][uid]
def update_user(uid,data):
    db["users"][str(uid)].update(data); save_data()
def is_member(uid):
    try:
        s1=bot.get_chat_member(f'@{CHANNEL1}',uid).status
        s2=bot.get_chat_member(f'@{CHANNEL2}',uid).status
        return s1 in ['member','administrator','creator'] and s2 in ['member','administrator','creator']
    except: return False
def count_successful_referrals(uid):
    uid=str(uid); c=0
    for ref in db["users"][uid].get("referrals_list",[]):
        if is_member(int(ref)): c+=1
    return c
def add_referral(rid,nid):
    rid,nid=str(rid),str(nid)
    if rid==nid: return
    if nid not in db["users"][rid].get("referrals_list",[]):
        db["users"][rid]["referrals_list"].append(nid); save_data()

def delete_previous_message(uid, cid):
    """پاک کردن پیام قبلی کاربر"""
    try:
        last_msg = db["users"].get(str(uid), {}).get("last_msg")
        if last_msg:
            bot.delete_message(cid, last_msg)
    except:
        pass

def send_new_message(uid, cid, text, reply_markup=None):
    """ارسال پیام جدید و ذخیره آیدی آن"""
    delete_previous_message(uid, cid)
    msg = bot.send_message(cid, text, reply_markup=reply_markup)
    db["users"][str(uid)]["last_msg"] = msg.message_id
    save_data()
    return msg

def get_text(key, lang, **kwargs):
    texts = {
        'promotion': {
            'fa': "✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌\n\n🔥 karbawzi UPD\nفراتر از یه بات ساده...\nاینجا فقط بات نیست، یک گوشه از هزاران رد پای من هست.\n\n👤 ادمین: @Karbawzi1PV\n📢 کانال اول: @Karbawzi1File\n🔒 کانال دوم: @Karbawzi1Trust\n\nما موندگاریم، چون متفاوتیم.",
            'en': fancy_text("✨ KARBAWZI PREMIUM\n\n🔥 karbawzi UPD\nMore than a simple bot...\nThis is not just a bot, it's a corner of thousands of my footprints.\n\n👤 Admin: @Karbawzi1PV\n📢 Channel 1: @Karbawzi1File\n🔒 Channel 2: @Karbawzi1Trust\n\nWe stay, because we are different.")
        },
        'choose_lang': {
            'fa': '🌍 زبان خود را انتخاب کنید:',
            'en': fancy_text('🌍 Choose your language:')
        },
        'welcome_main': {
            'fa': '✨ به پنل اصلی خوش اومدی!',
            'en': fancy_text('✨ Welcome to Main Panel!')
        },
        'dns_free_active': {
            'fa': '✅ تست رایگان فعال\n\nپرایمری: `78.157.53.52`\nثانویه: `78.157.53.219`\n\n⏳ {time} باقی‌مانده',
            'en': fancy_text('✅ Free test active\n\nPrimary: `78.157.53.52`\nSecondary: `78.157.53.219`\n\n⏳ {time} left')
        },
        'dns_public_note': {
            'fa': '🌍 DNS عمومی رایگان',
            'en': fancy_text('🌍 Public free DNS')
        },
        'referral_link': {
            'fa': '🔗 لینک معرفی شما:\n`https://t.me/{bot}?start={ref}`',
            'en': fancy_text('🔗 Your referral link:\n`https://t.me/{bot}?start={ref}`')
        },
        'account_credentials': {
            'fa': '📋 اکانت تست\n📧 `test@gmail.com`\n🔑 `test.`',
            'en': fancy_text('📋 Test account\n📧 `test@gmail.com`\n🔑 `test.`')
        },
        'update': {
            'fa': '🔄 در حال بروزرسانی',
            'en': fancy_text('🔄 Updating...')
        },
        'vip_title': {'fa': '💎 بخش VIP', 'en': fancy_text('💎 VIP Section')},
        'free_title': {'fa': '🎁 بخش رایگان', 'en': fancy_text('🎁 Free Section')},
        'gaming_title': {'fa': '🎮 بخش گیمینگ', 'en': fancy_text('🎮 Gaming Section')},
        'dns_title': {'fa': '🌐 بخش DNS', 'en': fancy_text('🌐 DNS Section')},
        'wireguard_title': {'fa': '🔐 بخش وایرگارد', 'en': fancy_text('🔐 Wireguard Section')},
        'codm_title': {'fa': '🆓 بخش کالاف دیوتی', 'en': fancy_text('🆓 CODM Section')},
    }
    return texts.get(key, {}).get(lang, '').format(**kwargs)

# ========== کیبوردهای ریپلی ==========

def language_keyboard():
    """کیبورد انتخاب زبان"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🇮🇷 فارسی"),
        KeyboardButton("🇬🇧 English")
    )
    return markup

def main_menu_keyboard(lang):
    """منوی اصلی با ریپلی کیبورد"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'fa':
        buttons = [
            KeyboardButton("💎 VIP"),
            KeyboardButton("🎁 فایل رایگان"),
            KeyboardButton("🎮 گیمینگ"),
            KeyboardButton("🌐 DNS"),
            KeyboardButton("🔐 وایرگارد"),
            KeyboardButton("🆓 کالاف دیوتی"),
            KeyboardButton("🌍 تغییر زبان"),
            KeyboardButton("📢 کانال‌ها")
        ]
    else:
        buttons = [
            KeyboardButton(fancy_text("💎 VIP")),
            KeyboardButton(fancy_text("🎁 FREE")),
            KeyboardButton(fancy_text("🎮 GAMING")),
            KeyboardButton(fancy_text("🌐 DNS")),
            KeyboardButton(fancy_text("🔐 WIREGUARD")),
            KeyboardButton(fancy_text("🆓 CODM")),
            KeyboardButton(fancy_text("🌍 CHANGE LANGUAGE")),
            KeyboardButton(fancy_text("📢 CHANNELS"))
        ]
    
    markup.add(*buttons)
    return markup

def back_keyboard(lang):
    """کیبورد برگشت به منوی اصلی"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def dns_keyboard(lang):
    """کیبورد بخش DNS"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'fa':
        buttons = [
            KeyboardButton("📶 ایرانسل"),
            KeyboardButton("📶 همراه اول"),
            KeyboardButton("📶 مخابرات"),
            KeyboardButton("📶 شاتل"),
            KeyboardButton("🌍 DNS عمومی"),
            KeyboardButton("🧪 تست رایگان"),
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
    """کیبورد بخش وایرگارد"""
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

def category_keyboard(items, prefix, lang):
    """کیبورد برای دسته‌بندی‌های مختلف (VIP, رایگان, گیمینگ)"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    buttons = []
    for k, v in items.items():
        buttons.append(KeyboardButton(v[lang]))
    
    markup.add(*buttons)
    markup.add(KeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu")))
    return markup

def codm_keyboard(lang, uid):
    """کیبورد بخش کالاف دیوتی با اطلاعات وضعیت"""
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

# ========== دیکشنری‌های محتوا ==========

vip_files = {
    'promax': {'fa': '🚀 ProMax', 'en': '🚀 ProMax'},
    'topvip': {'fa': '👑 TopVIP', 'en': '👑 TopVIP'}
}
free_files = {
    'free': {'fa': '🎁 فایل رایگان', 'en': '🎁 Free File'}
}
gaming_clips = {
    'clip1': {'fa': '🎬 اسنیپر حرفه‌ای', 'en': '🎬 Pro Sniper'},
    'clip2': {'fa': '🔥 کلچ ۱vs۵', 'en': '🔥 1vs5 Clutch'}
}
dns_public_list = {
    'radar': {'fa': '🛡️ رادار', 'en': '🛡️ Radar'},
    'electro': {'fa': '⚡ الکترو', 'en': '⚡ Electro'},
    '403': {'fa': '🌍 403', 'en': '🌍 403'},
    'shekan': {'fa': '🔓 شکن', 'en': '🔓 Shekan'}
}

# ========== هندلرها ==========

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    cid = m.chat.id
    args = m.text.split()
    
    # بررسی ریفرال
    if len(args) > 1 and args[1].startswith('ref'):
        try:
            rid = args[1][3:]
            if rid != str(uid):
                add_referral(rid, uid)
                get_user(uid)["referred_by"] = rid
                save_data()
        except:
            pass
    
    # دریافت یا ایجاد کاربر
    user = get_user(uid)
    
    # پاک کردن پیام /start کاربر
    try:
        bot.delete_message(cid, m.message_id)
    except:
        pass
    
    # ارسال پیام خوش‌آمدگویی با کیبورد انتخاب زبان
    send_new_message(uid, cid, get_text('promotion', 'fa'), language_keyboard())

@bot.message_handler(func=lambda m: True)
def handle_messages(m):
    uid = m.from_user.id
    cid = m.chat.id
    text = m.text
    user = get_user(uid)
    lang = user.get("lang", 'fa')
    
    # پاک کردن پیام کاربر
    try:
        bot.delete_message(cid, m.message_id)
    except:
        pass
    
    # ===== انتخاب زبان =====
    if text in ['🇮🇷 فارسی', '🇬🇧 English']:
        new_lang = 'fa' if text == '🇮🇷 فارسی' else 'en'
        update_user(uid, {"lang": new_lang})
        lang = new_lang
        
        # متن انگیزشی هر ساعت
        now = time.time()
        last = db["last_motivation"].get(str(uid), 0)
        if now - last >= 3600:
            db["last_motivation"][str(uid)] = now
            save_data()
            bot.send_message(cid, random_motivation(lang))
        
        send_new_message(uid, cid, get_text('welcome_main', lang), main_menu_keyboard(lang))
    
    # ===== منوی اصلی =====
    elif text in ['🔙 برگشت به منوی اصلی', fancy_text("🔙 Back to Main Menu")]:
        send_new_message(uid, cid, get_text('welcome_main', lang), main_menu_keyboard(lang))
    
    elif text in ['📢 کانال‌ها', fancy_text("📢 CHANNELS")]:
        bot.answer_callback_query = lambda x: None  # dummy
        bot.send_message(cid, f"📢 @{CHANNEL1}\n🔒 @{CHANNEL2}")
        send_new_message(uid, cid, get_text('welcome_main', lang), main_menu_keyboard(lang))
    
    elif text in ['🌍 تغییر زبان', fancy_text("🌍 CHANGE LANGUAGE")]:
        send_new_message(uid, cid, get_text('choose_lang', lang), language_keyboard())
    
    # ===== منوی VIP =====
    elif text in ['💎 VIP', fancy_text("💎 VIP")]:
        send_new_message(uid, cid, get_text('vip_title', lang), category_keyboard(vip_files, 'vip', lang))
    
    elif text in [v['fa'] for v in vip_files.values()] or text in [fancy_text(v['en']) for v in vip_files.values()]:
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('vip_title', lang), category_keyboard(vip_files, 'vip', lang))
    
    # ===== منوی فایل رایگان =====
    elif text in ['🎁 فایل رایگان', fancy_text("🎁 FREE")]:
        send_new_message(uid, cid, get_text('free_title', lang), category_keyboard(free_files, 'free', lang))
    
    elif text in [v['fa'] for v in free_files.values()] or text in [fancy_text(v['en']) for v in free_files.values()]:
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('free_title', lang), category_keyboard(free_files, 'free', lang))
    
    # ===== منوی گیمینگ =====
    elif text in ['🎮 گیمینگ', fancy_text("🎮 GAMING")]:
        send_new_message(uid, cid, get_text('gaming_title', lang), category_keyboard(gaming_clips, 'gaming', lang))
    
    elif text in [v['fa'] for v in gaming_clips.values()] or text in [fancy_text(v['en']) for v in gaming_clips.values()]:
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('gaming_title', lang), category_keyboard(gaming_clips, 'gaming', lang))
    
    # ===== منوی DNS =====
    elif text in ['🌐 DNS', fancy_text("🌐 DNS")]:
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
    
    elif text in ['📶 ایرانسل', fancy_text("📶 Irancell")]:
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
    
    elif text in ['📶 همراه اول', fancy_text("📶 MCI")]:
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
    
    elif text in ['📶 مخابرات', fancy_text("📶 Mokhaberat")]:
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
    
    elif text in ['📶 شاتل', fancy_text("📶 Shatel")]:
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
    
    elif text in ['🌍 DNS عمومی', fancy_text("🌍 Public DNS")]:
        txt = get_text('dns_public_note', lang) + "\n" + "\n".join(f"• {v[lang]}" for v in dns_public_list.values())
        bot.send_message(cid, txt)
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
    
    elif text in ['🧪 تست رایگان', fancy_text("🧪 Free Test")]:
        now = time.time()
        uid_str = str(uid)
        if uid_str in db["dns_free"]:
            rem = 6*3600 - (now - db["dns_free"][uid_str])
            if rem > 0:
                h = int(rem//3600)
                m = int((rem%3600)//60)
                ts = f"{h}h {m}m" if lang == 'en' else f"{h} ساعت {m} دقیقه"
                bot.send_message(cid, get_text('dns_free_active', lang, time=ts), parse_mode='Markdown')
                send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
                return
            else:
                del db["dns_free"][uid_str]
                save_data()
        
        db["dns_free"][uid_str] = now
        save_data()
        ts = "6h 0m" if lang == 'en' else "6 ساعت 0 دقیقه"
        bot.send_message(cid, get_text('dns_free_active', lang, time=ts), parse_mode='Markdown')
        send_new_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang))
    
    # ===== منوی وایرگارد =====
    elif text in ['🔐 وایرگارد', fancy_text("🔐 WIREGUARD")]:
        send_new_message(uid, cid, get_text('wireguard_title', lang), wireguard_keyboard(lang))
    
    elif text in ['🔐 VPN', fancy_text("🔐 VPN")]:
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('wireguard_title', lang), wireguard_keyboard(lang))
    
    elif text in ['🌐 DNS', fancy_text("🌐 DNS")] and user.get("current_menu") == "wireguard":
        bot.send_message(cid, get_text('update', lang))
        send_new_message(uid, cid, get_text('wireguard_title', lang), wireguard_keyboard(lang))
    
    # ===== منوی کالاف دیوتی =====
    elif text in ['🆓 کالاف دیوتی', fancy_text("🆓 CODM")]:
        update_user(uid, {"current_menu": "codm"})
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
    
    elif text.startswith('🎮 اکانت رایگان') or text.startswith(fancy_text('🎮 Free Account')):
        if not is_member(uid):
            bot.answer_callback_query = lambda x: None
            bot.send_message(cid, "❌ ابتدا عضو کانال‌ها شوید" if lang == 'fa' else "❌ Join channels first")
            send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
            return
            
        cnt = count_successful_referrals(uid)
        if cnt >= 5:
            if not user["claimed"]["free_account"]:
                bot.send_message(cid, get_text('account_credentials', lang), parse_mode='Markdown')
                db["users"][str(uid)]["claimed"]["free_account"] = True
                save_data()
            else:
                bot.send_message(cid, "⚠️ قبلاً دریافت کردید" if lang == 'fa' else "⚠️ Already claimed")
        else:
            bot.send_message(cid, f"❌ نیاز به {5-cnt} دعوت دیگر" if lang == 'fa' else f"❌ Need {5-cnt} more invites")
        
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
    
    elif text.startswith('🔥 Artery') or text.startswith(fancy_text('🔥 Artery')):
        if not is_member(uid):
            bot.send_message(cid, "❌ ابتدا عضو کانال‌ها شوید" if lang == 'fa' else "❌ Join channels first")
            send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
            return
            
        cnt = count_successful_referrals(uid)
        if cnt >= 10:
            if not user["claimed"]["artery"]:
                bot.send_message(cid, get_text('account_credentials', lang), parse_mode='Markdown')
                db["users"][str(uid)]["claimed"]["artery"] = True
                save_data()
            else:
                bot.send_message(cid, "⚠️ قبلاً دریافت کردید" if lang == 'fa' else "⚠️ Already claimed")
        else:
            bot.send_message(cid, f"❌ نیاز به {10-cnt} دعوت دیگر" if lang == 'fa' else f"❌ Need {10-cnt} more invites")
        
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
    
    elif text.startswith('✨ Vivan Harris') or text.startswith(fancy_text('✨ Vivan Harris')):
        if not is_member(uid):
            bot.send_message(cid, "❌ ابتدا عضو کانال‌ها شوید" if lang == 'fa' else "❌ Join channels first")
            send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
            return
            
        cnt = count_successful_referrals(uid)
        if cnt >= 15:
            if not user["claimed"]["vivan"]:
                bot.send_message(cid, get_text('account_credentials', lang), parse_mode='Markdown')
                db["users"][str(uid)]["claimed"]["vivan"] = True
                save_data()
            else:
                bot.send_message(cid, "⚠️ قبلاً دریافت کردید" if lang == 'fa' else "⚠️ Already claimed")
        else:
            bot.send_message(cid, f"❌ نیاز به {15-cnt} دعوت دیگر" if lang == 'fa' else f"❌ Need {15-cnt} more invites")
        
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
    
    elif text in ['📋 لیست کمبو', fancy_text("📋 Combo List")]:
        if not is_member(uid):
            bot.send_message(cid, "❌ ابتدا عضو کانال‌ها شوید" if lang == 'fa' else "❌ Join channels first")
        else:
            bot.send_message(cid, f"👤 {ADMIN_ID}")
        
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))
    
    elif text in ['🔗 لینک معرفی', fancy_text("🔗 Referral Link")]:
        bot.send_message(cid, get_text('referral_link', lang, bot=BOT_USERNAME, ref=user["ref_code"]), parse_mode='Markdown')
        send_new_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid))

print("🚀 Bot is running with REPLY KEYBOARD...")
bot.polling(none_stop=True, interval=0, timeout=30)