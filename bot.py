import telebot, os, random, json, time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')
bot = telebot.TeleBot(TOKEN)
CHANNEL1, CHANNEL2, ADMIN_ID, BOT_USERNAME = 'Karbawzi1File', 'Karbawzi1Trust', '@Karbawzi1PV', 'YourBotUsername'

# ========== متن‌های انگیزشی ==========
MOTIVATION_FA = [
    "「انسان همان‌طور فکر می‌کند که زندگی می‌کند، نه همان‌طور که زندگی می‌کند فکر می‌کند。」 — ریلکه",
    "「عمیق‌ترین چاه‌ها، خاموش‌ترین آب‌ها را دارند。」 — ضرب‌المثل آلمانی",
    "「ستاره‌ها را نمی‌بینیم مگر اینکه شب شود。」 — مثل هندی",
    "「کوه‌ها را جابه‌جا نمی‌کنیم، راهی دورشان پیدا می‌کنیم。」 — فریدریش نیچه",
    "「بعضی کتاب‌ها را باید چشید، بعضی را بلعید، و بعضی را جوید و هضم کرد。」 — فرانسیس بیکن",
    "「هنر بزرگ این نیست که در میان طوفان زنده بمانی، بلکه این است که در میان طوفان برقصی。」 — ضرب‌المثل آفریقایی",
    "「ما زخم‌هایمان را در سکوت حمل می‌کنیم، نه در فریاد。」 — آنتوان چخوف",
    "「خورشید هر روز غروب می‌کند تا ما قدر طلوع را بدانیم。」 — مثل ژاپنی",
    "「مرز بین نبوغ و دیوانگی فقط با میزان موفقیت سنجیده می‌شود。」 — آرتور شوپنهاور",
    "「بعضی دیوارها نه برای دور نگه‌داشتن ما، بلکه برای محک زدن عزم ما ساخته شده‌اند。」 — ناشناس",
    "「ذهن مانند چتر نجات است؛ وقتی باز نباشد، کار نمی‌کند。」 — فرانک زاپا",
    "「تجربه معلمی سخت‌گیر است؛ اول امتحان می‌گیرد، بعد درس می‌دهد。」 — مثل انگلیسی",
    "「بزرگ‌ترین ماجراجویی‌ها در ذهن اتفاق می‌افتند، اما پاهایت باید آنها را دنبال کنند。」 — ناشناس",
    "「ما بردگان ابزارهای خود شده‌ایم。」 — ژان بودریار",
    "「پیشرفت غیرممکن نیست؛ فقط هنوز انجام نشده است。」 — ناشناس"
]

MOTIVATION_EN = [
    "💭 \"We are what we repeatedly do. Excellence, then, is not an act, but a habit.\" — Aristotle",
    "💭 \"The cave you fear to enter holds the treasure you seek.\" — Joseph Campbell",
    "💭 \"No tree, it is said, can grow to heaven unless its roots reach down to hell.\" — Carl Jung",
    "💭 \"The mystery of human existence lies not in just staying alive, but in finding something to live for.\" — Dostoevsky",
    "💭 \"We suffer more in imagination than in reality.\" — Seneca",
    "💭 \"The privilege of a lifetime is to become who you truly are.\" — Carl Jung",
    "💭 \"He who has a why to live can bear almost any how.\" — Nietzsche",
    "💭 \"Sometimes people don't want to hear the truth because they don't want their illusions destroyed.\" — Nietzsche",
    "💭 \"The most common way people give up their power is by thinking they don't have any.\" — Alice Walker",
    "💭 \"It is not the strongest of the species that survives, nor the most intelligent, but the one most responsive to change.\" — Leon C. Megginson",
    "💭 \"The two most important days in your life are the day you are born and the day you find out why.\" — Mark Twain",
    "💭 \"What is to give light must endure burning.\" — Viktor Frankl",
    "💭 \"Man is the only creature who refuses to be what he is.\" — Albert Camus",
    "💭 \"The wound is the place where the Light enters you.\" — Rumi",
    "💭 \"And now here is my secret, a very simple secret: It is only with the heart that one can see rightly; what is essential is invisible to the eye.\" — Saint-Exupéry"
]

def random_motivation(lang):
    return random.choice(MOTIVATION_FA if lang=='fa' else MOTIVATION_EN)

# ========== دیتابیس ==========
DATA_FILE='bot_data.json'
def load_data():
    try:
        with open(DATA_FILE,'r',encoding='utf-8') as f: return json.load(f)
    except: return {"users":{},"dns_free":{},"last_motivation":{},"pinned_messages":{}}
db=load_data()
def save_data(): 
    with open(DATA_FILE,'w',encoding='utf-8') as f: json.dump(db,f,ensure_ascii=False,indent=2)

def get_user(uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"lang":"fa","ref_code":f"ref{uid}","referred_by":None,"referrals_list":[],"claimed":{"free_account":False,"artery":False,"vivan":False,"combo":False}}
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

def pin_motivation(uid, cid, lang):
    """سنجاق کردن متن انگیزشی"""
    try:
        # پاک کردن پیام سنجاق شده قبلی
        if str(uid) in db["pinned_messages"]:
            try:
                bot.unpin_chat_message(cid, db["pinned_messages"][str(uid)])
            except:
                pass
        
        # ارسال و سنجاق متن جدید
        msg = bot.send_message(cid, random_motivation(lang))
        bot.pin_chat_message(cid, msg.message_id, disable_notification=True)
        db["pinned_messages"][str(uid)] = msg.message_id
        save_data()
    except:
        pass

# ========== متن‌ها ==========
def get_text(key, lang, **kwargs):
    texts = {
        'promotion': {
            'fa': "✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 ✨\n\n🔥 karbawzi UPD\nفراتر از یه بات ساده...\nاینجا فقط بات نیست، یک گوشه از هزاران رد پای من هست.\n\n👤 ادمین: @Karbawzi1PV\n📢 کانال اول: @Karbawzi1File\n🔒 کانال دوم: @Karbawzi1Trust\n\nما موندگاریم، چون متفاوتیم.",
            'en': "✨ KARBAWZI PREMIUM ✨\n\n🔥 karbawzi UPD\nMore than a simple bot...\nThis is not just a bot, it's a corner of thousands of my footprints.\n\n👤 Admin: @Karbawzi1PV\n📢 Channel 1: @Karbawzi1File\n🔒 Channel 2: @Karbawzi1Trust\n\nWe stay, because we are different."
        },
        'choose_lang': {
            'fa': '🌍 زبان خود را انتخاب کنید:',
            'en': '🌍 Choose your language:'
        },
        'welcome_main': {
            'fa': '✨ به پنل اصلی خوش اومدی!',
            'en': '✨ Welcome to Main Panel!'
        },
        'dns_free_active': {
            'fa': '✅ تست رایگان فعال\n\nپرایمری: `78.157.53.52`\nثانویه: `78.157.53.219`\n\n⏳ {time} باقی‌مانده',
            'en': '✅ Free test active\n\nPrimary: `78.157.53.52`\nSecondary: `78.157.53.219`\n\n⏳ {time} left'
        },
        'dns_public_note': {
            'fa': '🌍 DNS عمومی رایگان',
            'en': '🌍 Public free DNS'
        },
        'referral_link': {
            'fa': '🔗 لینک معرفی شما:\n`https://t.me/{bot}?start={ref}`',
            'en': '🔗 Your referral link:\n`https://t.me/{bot}?start={ref}`'
        },
        'account_credentials': {
            'fa': '📋 اکانت تست\n📧 `test@gmail.com`\n🔑 `test.`',
            'en': '📋 Test account\n📧 `test@gmail.com`\n🔑 `test.`'
        },
        'update': {
            'fa': '🔄 در حال بروزرسانی',
            'en': '🔄 Updating...'
        },
        'already_claimed': {
            'fa': '⚠️ قبلاً دریافت کردید',
            'en': '⚠️ Already claimed'
        },
        'not_member': {
            'fa': '❌ ابتدا عضو کانال‌ها شوید',
            'en': '❌ Join channels first'
        }
    }
    return texts.get(key, {}).get(lang, '').format(**kwargs)

# ========== کیبوردهای رنگی ==========
def color_button(text, color_code=None):
    """ایجاد دکمه رنگی (با ایموجی‌های رنگی)"""
    # استفاده از ایموجی‌های رنگی برای جلوه بهتر
    colored = {
        '💎': '💎',
        '🎁': '🎁',
        '🎮': '🎮',
        '🌐': '🌐',
        '🔐': '🔐',
        '🆓': '🆓',
        '📢': '📢',
        '🌍': '🌍',
        '🔙': '🔙',
        '📶': '📶',
        '🧪': '🧪',
        '🔥': '🔥',
        '✨': '✨',
        '📋': '📋',
        '🔗': '🔗',
        '✅': '✅',
        '❌': '❌'
    }
    return text

def language_keyboard():
    """کیبورد انتخاب زبان"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🇮🇷 فارسی"),
        KeyboardButton("🇬🇧 English")
    )
    return markup

def main_menu_keyboard(lang):
    """منوی اصلی با دکمه‌های رنگی"""
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
            KeyboardButton("💎 VIP"),
            KeyboardButton("🎁 FREE"),
            KeyboardButton("🎮 GAMING"),
            KeyboardButton("🌐 DNS"),
            KeyboardButton("🔐 WIREGUARD"),
            KeyboardButton("🆓 CODM"),
            KeyboardButton("🌍 LANGUAGE"),
            KeyboardButton("📢 CHANNELS")
        ]
    
    markup.add(*buttons)
    return markup

def dns_keyboard(lang):
    """کیبورد DNS"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'fa':
        buttons = [
            KeyboardButton("📶 ایرانسل"),
            KeyboardButton("📶 همراه اول"),
            KeyboardButton("📶 مخابرات"),
            KeyboardButton("📶 شاتل"),
            KeyboardButton("🌍 DNS عمومی"),
            KeyboardButton("🧪 تست رایگان"),
            KeyboardButton("🔙 منوی اصلی")
        ]
    else:
        buttons = [
            KeyboardButton("📶 Irancell"),
            KeyboardButton("📶 MCI"),
            KeyboardButton("📶 Mokhaberat"),
            KeyboardButton("📶 Shatel"),
            KeyboardButton("🌍 Public DNS"),
            KeyboardButton("🧪 Free Test"),
            KeyboardButton("🔙 Main Menu")
        ]
    
    markup.add(*buttons)
    return markup

def wireguard_keyboard(lang):
    """کیبورد وایرگارد"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'fa':
        buttons = [
            KeyboardButton("🔐 VPN"),
            KeyboardButton("🌐 DNS"),
            KeyboardButton("🔙 منوی اصلی")
        ]
    else:
        buttons = [
            KeyboardButton("🔐 VPN"),
            KeyboardButton("🌐 DNS"),
            KeyboardButton("🔙 Main Menu")
        ]
    
    markup.add(*buttons)
    return markup

def category_keyboard(items, lang):
    """کیبورد دسته‌بندی"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    buttons = []
    for item in items.values():
        buttons.append(KeyboardButton(item[lang]))
    
    markup.add(*buttons)
    markup.add(KeyboardButton("🔙 منوی اصلی" if lang == 'fa' else "🔙 Main Menu"))
    return markup

def codm_keyboard(lang, uid):
    """کیبورد کالاف با اطلاعات وضعیت"""
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
            KeyboardButton("🔙 منوی اصلی")
        ]
    else:
        free_text = f"🎮 Free Account {'✅' if is_mem else '❌'} | {cnt}/5"
        artery_text = f"🔥 Artery {'✅' is is_mem else '❌'} | {cnt}/10"
        vivan_text = f"✨ Vivan Harris {'✅' if is_mem else '❌'} | {cnt}/15"
        
        buttons = [
            KeyboardButton(free_text),
            KeyboardButton(artery_text),
            KeyboardButton(vivan_text),
            KeyboardButton("📋 Combo List"),
            KeyboardButton("🔗 Referral Link"),
            KeyboardButton("🔙 Main Menu")
        ]
    
    markup.add(*buttons)
    return markup

# ========== محتوا ==========
vip_files = {
    'promax': {'fa': '🚀 ProMax', 'en': '🚀 ProMax'},
    'topvip': {'fa': '👑 TopVIP', 'en': '👑 TopVIP'}
}
free_files = {
    'free': {'fa': '🎁 فایل رایگان', 'en': '🎁 Free File'}
}
gaming_clips = {
    'clip1': {'fa': '🎬 اسنیپر', 'en': '🎬 Sniper'},
    'clip2': {'fa': '🔥 کلچ', 'en': '🔥 Clutch'}
}
dns_public_list = {
    'radar': {'fa': '🛡️ رادار', 'en': '🛡️ Radar'},
    'electro': {'fa': '⚡ الکترو', 'en': '⚡ Electro'}
}

# ========== هندلرها ==========
@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    cid = m.chat.id
    args = m.text.split()
    
    # ریفرال
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
    
    # ارسال متن انگیزشی و سنجاق آن
    pin_motivation(uid, cid, user['lang'])
    
    # ارسال پیام خوش‌آمدگویی
    bot.send_message(
        cid, 
        get_text('promotion', user['lang']),
        reply_markup=main_menu_keyboard(user['lang']) if user['lang'] else language_keyboard()
    )

@bot.message_handler(func=lambda m: True)
def handle_all(m):
    uid = m.from_user.id
    cid = m.chat.id
    text = m.text
    user = get_user(uid)
    lang = user.get("lang", 'fa')
    
    # بررسی متن انگیزشی هر ساعت
    now = time.time()
    last = db["last_motivation"].get(str(uid), 0)
    if now - last >= 3600:
        db["last_motivation"][str(uid)] = now
        save_data()
        pin_motivation(uid, cid, lang)
    
    # ===== انتخاب زبان =====
    if text in ['🇮🇷 فارسی', '🇬🇧 English']:
        new_lang = 'fa' if text == '🇮🇷 فارسی' else 'en'
        update_user(uid, {"lang": new_lang})
        lang = new_lang
        
        bot.send_message(
            cid,
            get_text('welcome_main', lang),
            reply_markup=main_menu_keyboard(lang)
        )
    
    # ===== برگشت به منوی اصلی =====
    elif text in ['🔙 منوی اصلی', '🔙 Main Menu']:
        bot.send_message(
            cid,
            get_text('welcome_main', lang),
            reply_markup=main_menu_keyboard(lang)
        )
    
    # ===== کانال‌ها =====
    elif text in ['📢 کانال‌ها', '📢 CHANNELS']:
        bot.send_message(
            cid,
            f"📢 @{CHANNEL1}\n🔒 @{CHANNEL2}",
            reply_markup=main_menu_keyboard(lang)
        )
    
    # ===== تغییر زبان =====
    elif text in ['🌍 تغییر زبان', '🌍 LANGUAGE']:
        bot.send_message(
            cid,
            get_text('choose_lang', lang),
            reply_markup=language_keyboard()
        )
    
    # ===== منوها =====
    elif text in ['💎 VIP', '💎 VIP']:
        bot.send_message(
            cid,
            "💎",
            reply_markup=category_keyboard(vip_files, lang)
        )
    
    elif text in ['🎁 فایل رایگان', '🎁 FREE']:
        bot.send_message(
            cid,
            "🎁",
            reply_markup=category_keyboard(free_files, lang)
        )
    
    elif text in ['🎮 گیمینگ', '🎮 GAMING']:
        bot.send_message(
            cid,
            "🎮",
            reply_markup=category_keyboard(gaming_clips, lang)
        )
    
    elif text in ['🌐 DNS', '🌐 DNS']:
        bot.send_message(
            cid,
            "🌐",
            reply_markup=dns_keyboard(lang)
        )
    
    elif text in ['🔐 وایرگارد', '🔐 WIREGUARD']:
        bot.send_message(
            cid,
            "🔐",
            reply_markup=wireguard_keyboard(lang)
        )
    
    elif text in ['🆓 کالاف دیوتی', '🆓 CODM']:
        bot.send_message(
            cid,
            "🆓",
            reply_markup=codm_keyboard(lang, uid)
        )
    
    # ===== DNS =====
    elif text in ['📶 ایرانسل', '📶 Irancell',
                  '📶 همراه اول', '📶 MCI',
                  '📶 مخابرات', '📶 Mokhaberat',
                  '📶 شاتل', '📶 Shatel']:
        bot.send_message(cid, get_text('update', lang))
        bot.send_message(
            cid,
            "🌐",
            reply_markup=dns_keyboard(lang)
        )
    
    elif text in ['🌍 DNS عمومی', '🌍 Public DNS']:
        txt = get_text('dns_public_note', lang) + "\n\n"
        txt += "\n".join(f"• {v[lang]}" for v in dns_public_list.values())
        bot.send_message(cid, txt)
        bot.send_message(
            cid,
            "🌐",
            reply_markup=dns_keyboard(lang)
        )
    
    elif text in ['🧪 تست رایگان', '🧪 Free Test']:
        now = time.time()
        uid_str = str(uid)
        
        if uid_str in db["dns_free"]:
            rem = 6*3600 - (now - db["dns_free"][uid_str])
            if rem > 0:
                h = int(rem//3600)
                m = int((rem%3600)//60)
                ts = f"{h}h {m}m" if lang == 'en' else f"{h} ساعت {m} دقیقه"
                bot.send_message(
                    cid,
                    get_text('dns_free_active', lang, time=ts),
                    parse_mode='Markdown'
                )
                bot.send_message(
                    cid,
                    "🌐",
                    reply_markup=dns_keyboard(lang)
                )
                return
            else:
                del db["dns_free"][uid_str]
                save_data()
        
        db["dns_free"][uid_str] = now
        save_data()
        ts = "6h 0m" if lang == 'en' else "6 ساعت 0 دقیقه"
        bot.send_message(
            cid,
            get_text('dns_free_active', lang, time=ts),
            parse_mode='Markdown'
        )
        bot.send_message(
            cid,
            "🌐",
            reply_markup=dns_keyboard(lang)
        )
    
    # ===== وایرگارد =====
    elif text in ['🔐 VPN', '🌐 DNS']:
        bot.send_message(cid, get_text('update', lang))
        bot.send_message(
            cid,
            "🔐",
            reply_markup=wireguard_keyboard(lang)
        )
    
    # ===== کالاف =====
    elif text.startswith(('🎮 اکانت رایگان', '🎮 Free Account')):
        if not is_member(uid):
            bot.send_message(cid, get_text('not_member', lang))
            bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
            return
        
        cnt = count_successful_referrals(uid)
        if cnt >= 5:
            if not user["claimed"]["free_account"]:
                bot.send_message(cid, get_text('account_credentials', lang), parse_mode='Markdown')
                user["claimed"]["free_account"] = True
                save_data()
            else:
                bot.send_message(cid, get_text('already_claimed', lang))
        else:
            bot.send_message(cid, f"❌ نیاز به {5-cnt} دعوت دیگر" if lang == 'fa' else f"❌ Need {5-cnt} more invites")
        
        bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
    
    elif text.startswith(('🔥 Artery')):
        if not is_member(uid):
            bot.send_message(cid, get_text('not_member', lang))
            bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
            return
        
        cnt = count_successful_referrals(uid)
        if cnt >= 10:
            if not user["claimed"]["artery"]:
                bot.send_message(cid, get_text('account_credentials', lang), parse_mode='Markdown')
                user["claimed"]["artery"] = True
                save_data()
            else:
                bot.send_message(cid, get_text('already_claimed', lang))
        else:
            bot.send_message(cid, f"❌ نیاز به {10-cnt} دعوت دیگر" if lang == 'fa' else f"❌ Need {10-cnt} more invites")
        
        bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
    
    elif text.startswith(('✨ Vivan Harris')):
        if not is_member(uid):
            bot.send_message(cid, get_text('not_member', lang))
            bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
            return
        
        cnt = count_successful_referrals(uid)
        if cnt >= 15:
            if not user["claimed"]["vivan"]:
                bot.send_message(cid, get_text('account_credentials', lang), parse_mode='Markdown')
                user["claimed"]["vivan"] = True
                save_data()
            else:
                bot.send_message(cid, get_text('already_claimed', lang))
        else:
            bot.send_message(cid, f"❌ نیاز به {15-cnt} دعوت دیگر" if lang == 'fa' else f"❌ Need {15-cnt} more invites")
        
        bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
    
    elif text in ['📋 لیست کمبو', '📋 Combo List']:
        if not is_member(uid):
            bot.send_message(cid, get_text('not_member', lang))
        else:
            bot.send_message(cid, f"👤 {ADMIN_ID}")
        
        bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
    
    elif text in ['🔗 لینک معرفی', '🔗 Referral Link']:
        bot.send_message(
            cid,
            get_text('referral_link', lang, bot=BOT_USERNAME, ref=user["ref_code"]),
            parse_mode='Markdown'
        )
        bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
    
    # ===== آیتم‌های VIP =====
    elif text in [v['fa'] for v in vip_files.values()] or text in [v['en'] for v in vip_files.values()]:
        bot.send_message(cid, get_text('update', lang))
        bot.send_message(cid, "💎", reply_markup=category_keyboard(vip_files, lang))
    
    # ===== آیتم‌های رایگان =====
    elif text in [v['fa'] for v in free_files.values()] or text in [v['en'] for v in free_files.values()]:
        bot.send_message(cid, get_text('update', lang))
        bot.send_message(cid, "🎁", reply_markup=category_keyboard(free_files, lang))
    
    # ===== آیتم‌های گیمینگ =====
    elif text in [v['fa'] for v in gaming_clips.values()] or text in [v['en'] for v in gaming_clips.values()]:
        bot.send_message(cid, get_text('update', lang))
        bot.send_message(cid, "🎮", reply_markup=category_keyboard(gaming_clips, lang))

print("🚀 Bot is running with Reply Keyboard & Pinned Messages...")
bot.polling(none_stop=True)