import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import random
import json
import time
from datetime import datetime, timedelta

# ========== تنظیمات اولیه ==========
TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')
bot = telebot.TeleBot(TOKEN)

CHANNEL1 = 'Karbawzi1File'
CHANNEL2 = 'Karbawzi1Trust'
ADMIN_ID = '@Karbawzi1PV'
BOT_USERNAME = 'YourBotUsername'  # حتماً اینو با یوزرنیم خودت عوض کن!

# ========== فونت انگلیسی خاص (Math Bold Sans) ==========
def fancy_text(text):
    """تبدیل متن انگلیسی به فونت 𝙼𝚊𝚝𝚑 𝙱𝚘𝚕𝚍 𝚂𝚊𝚗𝚜 (خوانا و خفن)"""
    mapping = {
        'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴',
        'F': '𝙵', 'G': '𝙶', 'H': '𝙷', 'I': '𝙸', 'J': '𝙹',
        'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾',
        'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃',
        'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈',
        'Z': '𝚉',
        'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎',
        'f': '𝚏', 'g': '𝚐', 'h': '𝚑', 'i': '𝚒', 'j': '𝚓',
        'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗', 'o': '𝚘',
        'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝',
        'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢',
        'z': '𝚣'
    }
    return ''.join(mapping.get(ch, ch) for ch in text)

# ========== متن‌های انگیزشی عمیق (غیرکلیشه‌ای) ==========
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
    return random.choice(MOTIVATION_FA if lang == 'fa' else MOTIVATION_EN)

# ========== دیتابیس فایل JSON ==========
DATA_FILE = 'bot_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": {}, "dns_free": {}, "referral_codes": {}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db = load_data()

# ========== توابع کمکی برای کاربران ==========
def get_user(user_id):
    user_id = str(user_id)
    if user_id not in db["users"]:
        db["users"][user_id] = {
            "lang": "fa",
            "ref_code": f"ref{user_id}",
            "referred_by": None,
            "referrals_count": 0,
            "referrals_list": [],
            "claimed": {
                "free_account": False,
                "artery": False,
                "vivan": False,
                "combo": False
            }
        }
        save_data(db)
    return db["users"][user_id]

def update_user(user_id, data):
    user_id = str(user_id)
    db["users"][user_id].update(data)
    save_data(db)

def count_successful_referrals(user_id):
    """تعداد افرادی که توسط این کاربر دعوت شدن و عضو هر دو کانال هستند"""
    user_id = str(user_id)
    user = get_user(user_id)
    count = 0
    for ref_id in user.get("referrals_list", []):
        if is_member(int(ref_id)):
            count += 1
    return count

def add_referral(referrer_id, new_user_id):
    referrer_id = str(referrer_id)
    new_user_id = str(new_user_id)
    if referrer_id == new_user_id:
        return
    referrer = get_user(referrer_id)
    if new_user_id not in referrer.get("referrals_list", []):
        referrer["referrals_list"].append(new_user_id)
        # به‌روزرسانی شمارش در لحظه (اختیاری)
        referrer["referrals_count"] = count_successful_referrals(referrer_id)
        save_data(db)

# ========== بررسی عضویت در کانال‌ها ==========
def is_member(user_id):
    try:
        status1 = bot.get_chat_member(f'@{CHANNEL1}', user_id).status
        status2 = bot.get_chat_member(f'@{CHANNEL2}', user_id).status
        return status1 in ['member', 'administrator', 'creator'] and status2 in ['member', 'administrator', 'creator']
    except:
        return False

# ========== متن‌های ثابت دوزبانه ==========
def get_text(key, lang):
    texts = {
        'promotion': {
            'fa': """
━━━━━━━━━━━━━━━━━━━━
✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐁𝐎𝐓 ✨
━━━━━━━━━━━━━━━━━━━━

🔥 فراتر از یه بات ساده...
اینجا فقط دانلود نیست، تجربه‌ست.

👤 ادمین: @Karbawzi1PV
📢 کانال فایل‌ها: @Karbawzi1File
🔒 کانال اعتماد: @Karbawzi1Trust

━━━━━━━━━━━━━━━━━━━━
ما موندگاریم، چون متفاوتیم.
━━━━━━━━━━━━━━━━━━━━
""",
            'en': fancy_text("""
━━━━━━━━━━━━━━━━━━━━
✨ KARBAWZI PREMIUM BOT ✨
━━━━━━━━━━━━━━━━━━━━

🔥 More than a simple bot...
This is not just download, it's an experience.

👤 Admin: @Karbawzi1PV
📢 Files Channel: @Karbawzi1File
🔒 Trust Channel: @Karbawzi1Trust

━━━━━━━━━━━━━━━━━━━━
We stay, because we are different.
━━━━━━━━━━━━━━━━━━━━
""")
        },
        'choose_lang': {
            'fa': "🌍 لطفاً زبان خود را انتخاب کنید:",
            'en': fancy_text("🌍 Please choose your language:")
        },
        'welcome_main': {
            'fa': "✨ به پنل اصلی خوش اومدی!\nیکی از دسته‌بندی‌های زیر رو انتخاب کن:",
            'en': fancy_text("✨ Welcome to Main Panel!\nChoose one of the categories below:")
        },
        'verified_membership': {
            'fa': "✅ تایید شدی! حالا به جمع حرفه‌ای‌ها خوش اومدی 🔥",
            'en': fancy_text("✅ Verified! Now welcome to the pros 🔥")
        },
        'not_member': {
            'fa': "❌ شما هنوز عضو کانال‌ها نشده‌اید!",
            'en': fancy_text("❌ You are not a member yet!")
        },
        'error': {
            'fa': "❌ خطا در ارسال فایل!",
            'en': fancy_text("❌ Error sending file!")
        },
        'channels_info': {
            'fa': "📢 @Karbawzi1File\n🔒 @Karbawzi1Trust",
            'en': fancy_text("📢 @Karbawzi1File\n🔒 @Karbawzi1Trust")
        },
        'update_message': {
            'fa': "🔄 در حال بروزرسانی بات هستیم.\nلطفاً شکیبا باشید و بعداً مراجعه کنید 🙏",
            'en': fancy_text("🔄 Bot is being updated.\nPlease be patient and check back later 🙏")
        },
        'prices_update': {
            'fa': "💰 قیمت‌ها در حال بروزرسانی می‌باشد.\nبه‌زودی با پیشنهادهای ویژه بازخواهیم گشت ✨",
            'en': fancy_text("💰 Prices are being updated.\nWe'll be back soon with special offers ✨")
        },
        'dns_free_title': {
            'fa': "🌐 تست رایگان DNS",
            'en': fancy_text("🌐 Free DNS Test")
        },
        'dns_free_active': {
            'fa': "✅ تست رایگان شما فعال است.\n\nپرایمری DNS: `78.157.53.52`\nثانویه DNS: `78.157.53.219`\n\n⏳ زمان باقی‌مانده: {time}\n\nپس از اتمام، می‌توانید مجدداً فعال کنید.",
            'en': fancy_text("✅ Your free test is active.\n\nPrimary DNS: `78.157.53.52`\nSecondary DNS: `78.157.53.219`\n\n⏳ Time left: {time}\n\nAfter expiration, you can activate again.")
        },
        'dns_free_expired': {
            'fa': "⏰ تست رایگان شما به پایان رسیده.\nمی‌توانید دوباره فعال کنید.",
            'en': fancy_text("⏰ Your free test has expired.\nYou can activate again.")
        },
        'dns_free_used': {
            'fa': "⚠️ شما قبلاً از تست رایگان استفاده کرده‌اید.\nلطفاً پس از اتمام زمان مجدداً تلاش کنید.",
            'en': fancy_text("⚠️ You have already used the free test.\nPlease try again after it expires.")
        },
        'dns_public_note': {
            'fa': "🌍 DNS عمومی و کاملاً رایگان – مناسب برای دور زدن محدودیت‌های ساده",
            'en': fancy_text("🌍 Public & completely free DNS – suitable for bypassing simple restrictions")
        },
        'codm_free_locked': {
            'fa': "🔒 برای دریافت اکانت رایگان باید:\n✅ عضو هر دو کانال شوید\n✅ ۵ نفر را با لینک معرفی خود دعوت کنید (دعوت‌شدگان نیز عضو کانال‌ها شوند)\n\nتعداد دعوت‌های موفق فعلی: {count}/5",
            'en': fancy_text("🔒 To get a free account:\n✅ Join both channels\n✅ Invite 5 people via your referral link (they must also join channels)\n\nCurrent successful invites: {count}/5")
        },
        'codm_artery_locked': {
            'fa': "🔒 برای دریافت اکانت Artery (هند، تک‌سیو) باید:\n✅ عضو هر دو کانال شوید\n✅ ۱۰ نفر را با لینک معرفی دعوت کنید\n\nتعداد دعوت‌های موفق فعلی: {count}/10",
            'en': fancy_text("🔒 To get an Artery account (India, single save):\n✅ Join both channels\n✅ Invite 10 people via your referral link\n\nCurrent successful invites: {count}/10")
        },
        'codm_vivan_locked': {
            'fa': "🔒 برای دریافت اکانت Vivan Harris (هند، تک‌سیو) باید:\n✅ عضو هر دو کانال شوید\n✅ ۱۵ نفر را با لینک معرفی دعوت کنید\n\nتعداد دعوت‌های موفق فعلی: {count}/15",
            'en': fancy_text("🔒 To get a Vivan Harris account (India, single save):\n✅ Join both channels\n✅ Invite 15 people via your referral link\n\nCurrent successful invites: {count}/15")
        },
        'codm_combo_locked': {
            'fa': "🔒 برای دریافت لیست کمبو باید عضو هر دو کانال باشید.\nپس از عضویت، با ادمین زیر هماهنگ کنید:\n👤 {admin}",
            'en': fancy_text("🔒 To get the combo list you must be a member of both channels.\nAfter joining, contact the admin:\n👤 {admin}")
        },
        'account_credentials': {
            'fa': "📋 اکانت شما:\n📧 Gmail: `test@gmail.com`\n🔑 Password: `test.`\n\n⚠️ این اکانت صرفاً برای تست می‌باشد و در آپدیت بعدی با اکانت واقعی جایگزین خواهد شد.",
            'en': fancy_text("📋 Your account:\n📧 Gmail: `test@gmail.com`\n🔑 Password: `test.`\n\n⚠️ This account is for testing only and will be replaced with real accounts in the next update.")
        },
        'no_accounts_left': {
            'fa': "😔 متأسفانه در حال حاضر هیچ اکانتی موجود نیست. بعداً تلاش کنید.",
            'en': fancy_text("😔 Unfortunately no accounts are available at the moment. Try later.")
        },
        'referral_link': {
            'fa': "🔗 لینک معرفی اختصاصی شما:\n`https://t.me/{bot}?start={ref}`\n\nاین لینک را برای دوستانتان بفرستید. هر نفر که عضو هر دو کانال شود، یک دعوت موفق برای شما حساب می‌شود.",
            'en': fancy_text("🔗 Your personal referral link:\n`https://t.me/{bot}?start={ref}`\n\nShare this link with your friends. Each person who joins both channels counts as a successful referral.")
        }
    }
    return texts.get(key, {}).get(lang, texts[key]['en'])

# ========== کیبوردها ==========
def language_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇮🇷 فارسی", callback_data='lang_fa'),
        InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')
    )
    return markup

def main_menu_keyboard(lang):
    markup = InlineKeyboardMarkup(row_width=2)
    if lang == 'fa':
        buttons = [
            InlineKeyboardButton("💎 VIP", callback_data='menu_vip'),
            InlineKeyboardButton("🎁 فایل رایگان", callback_data='menu_free'),
            InlineKeyboardButton("🎮 GAMING", callback_data='menu_gaming'),
            InlineKeyboardButton("🌐 DNS", callback_data='menu_dns'),
            InlineKeyboardButton("🔐 WIRE", callback_data='menu_wireguard'),
            InlineKeyboardButton("🆓 CODM", callback_data='menu_codm'),
            InlineKeyboardButton("🌍 زبان", callback_data='change_lang'),
            InlineKeyboardButton("📢 کانال‌ها", callback_data='channels')
        ]
    else:
        buttons = [
            InlineKeyboardButton(fancy_text("💎 VIP"), callback_data='menu_vip'),
            InlineKeyboardButton(fancy_text("🎁 FREE"), callback_data='menu_free'),
            InlineKeyboardButton(fancy_text("🎮 GAMING"), callback_data='menu_gaming'),
            InlineKeyboardButton(fancy_text("🌐 DNS"), callback_data='menu_dns'),
            InlineKeyboardButton(fancy_text("🔐 WIRE"), callback_data='menu_wireguard'),
            InlineKeyboardButton(fancy_text("🆓 CODM"), callback_data='menu_codm'),
            InlineKeyboardButton(fancy_text("🌍 LANGUAGE"), callback_data='change_lang'),
            InlineKeyboardButton(fancy_text("📢 CHANNELS"), callback_data='channels')
        ]
    markup.add(*buttons)
    return markup

def build_category_menu(category_dict, category_prefix, lang):
    markup = InlineKeyboardMarkup(row_width=2)
    for key, value in category_dict.items():
        name = value[lang]
        if lang == 'en':
            name = fancy_text(name)
        markup.add(InlineKeyboardButton(name, callback_data=f'{category_prefix}_{key}'))
    back_text = "🔙 برگشت" if lang == 'fa' else fancy_text("🔙 Back")
    markup.add(InlineKeyboardButton(back_text, callback_data='back_main'))
    return markup

def dns_main_keyboard(lang):
    """منوی اصلی DNS شامل اپراتورها، عمومی و تست رایگان"""
    markup = InlineKeyboardMarkup(row_width=2)
    if lang == 'fa':
        buttons = [
            InlineKeyboardButton("📶 ایرانسل (MTN)", callback_data='dns_operator_irancell'),
            InlineKeyboardButton("📶 همراه اول (MCI)", callback_data='dns_operator_mci'),
            InlineKeyboardButton("📶 مخابرات", callback_data='dns_operator_mokhaberat'),
            InlineKeyboardButton("📶 شاتل", callback_data='dns_operator_shatel'),
            InlineKeyboardButton("🌍 DNS عمومی", callback_data='dns_public'),
            InlineKeyboardButton("🧪 تست رایگان", callback_data='dns_free'),
        ]
    else:
        buttons = [
            InlineKeyboardButton(fancy_text("📶 Irancell (MTN)"), callback_data='dns_operator_irancell'),
            InlineKeyboardButton(fancy_text("📶 Hamrah Aval (MCI)"), callback_data='dns_operator_mci'),
            InlineKeyboardButton(fancy_text("📶 Mokhaberat"), callback_data='dns_operator_mokhaberat'),
            InlineKeyboardButton(fancy_text("📶 Shatel"), callback_data='dns_operator_shatel'),
            InlineKeyboardButton(fancy_text("🌍 Public DNS"), callback_data='dns_public'),
            InlineKeyboardButton(fancy_text("🧪 Free Test"), callback_data='dns_free'),
        ]
    markup.add(*buttons)
    back_text = "🔙 برگشت" if lang == 'fa' else fancy_text("🔙 Back")
    markup.add(InlineKeyboardButton(back_text, callback_data='back_main'))
    return markup

def wireguard_main_keyboard(lang):
    markup = InlineKeyboardMarkup(row_width=2)
    if lang == 'fa':
        buttons = [
            InlineKeyboardButton("🔐 Wire VPN", callback_data='wire_vpn'),
            InlineKeyboardButton("🌐 Wire DNS", callback_data='wire_dns'),
        ]
    else:
        buttons = [
            InlineKeyboardButton(fancy_text("🔐 Wire VPN"), callback_data='wire_vpn'),
            InlineKeyboardButton(fancy_text("🌐 Wire DNS"), callback_data='wire_dns'),
        ]
    markup.add(*buttons)
    back_text = "🔙 برگشت" if lang == 'fa' else fancy_text("🔙 Back")
    markup.add(InlineKeyboardButton(back_text, callback_data='back_main'))
    return markup

def codm_main_keyboard(lang):
    markup = InlineKeyboardMarkup(row_width=2)
    if lang == 'fa':
        buttons = [
            InlineKeyboardButton("🎮 اکانت رایگان", callback_data='codm_free'),
            InlineKeyboardButton("🔥 Artery", callback_data='codm_artery'),
            InlineKeyboardButton("✨ Vivan Harris", callback_data='codm_vivan'),
            InlineKeyboardButton("📋 لیست کمبو", callback_data='codm_combo'),
            InlineKeyboardButton("🔗 لینک معرفی", callback_data='codm_referral')
        ]
    else:
        buttons = [
            InlineKeyboardButton(fancy_text("🎮 Free Account"), callback_data='codm_free'),
            InlineKeyboardButton(fancy_text("🔥 Artery"), callback_data='codm_artery'),
            InlineKeyboardButton(fancy_text("✨ Vivan Harris"), callback_data='codm_vivan'),
            InlineKeyboardButton(fancy_text("📋 Combo List"), callback_data='codm_combo'),
            InlineKeyboardButton(fancy_text("🔗 Referral Link"), callback_data='codm_referral')
        ]
    markup.add(*buttons)
    back_text = "🔙 برگشت" if lang == 'fa' else fancy_text("🔙 Back")
    markup.add(InlineKeyboardButton(back_text, callback_data='back_main'))
    return markup

# ========== دیتای فایل‌ها و سرویس‌ها ==========
vip_files = {
    'promax': {'fa': '🚀 ProMax', 'en': '🚀 ProMax', 'version': '1.0.53.13', 'date': '2026-02-13', 'link': None},
    'topvip': {'fa': '👑 TopVIP', 'en': '👑 TopVIP', 'version': '1.0.53.13', 'date': '2026-02-13', 'link': None},
    'youtuber': {'fa': '🎬 YouTuber', 'en': '🎬 YouTuber', 'version': '1.0.53.13', 'date': '2026-02-13', 'link': None},
    'fixlag': {'fa': '⚡ FixLag (ضد لگ)', 'en': '⚡ FixLag', 'version': '1.0.53.13', 'date': '2026-02-13', 'link': None}
}

free_files = {
    'free': {'fa': '🎁 فایل رایگان', 'en': '🎁 Free File', 'version': '1.0.53.13', 'date': '2026-02-13', 'link': None}
}

gaming_clips = {
    'clip1': {'fa': '🎬 اسنیپر حرفه‌ای', 'en': '🎬 Pro Sniper', 'link': '#'},
    'clip2': {'fa': '🔥 کلچ ۱vs۵', 'en': '🔥 1vs5 Clutch', 'link': '#'},
    'clip3': {'fa': '🏆 تورنمنت هفته', 'en': '🏆 Weekly Tourney', 'link': '#'},
    'clip4': {'fa': '📺 آموزش حرکات', 'en': '📺 Movement Tips', 'link': '#'}
}

dns_operators = {
    'irancell': {'fa': '📶 ایرانسل (MTN)', 'en': '📶 Irancell (MTN)', 'link': '#'},
    'mci': {'fa': '📶 همراه اول (MCI)', 'en': '📶 Hamrah Aval (MCI)', 'link': '#'},
    'mokhaberat': {'fa': '📶 مخابرات', 'en': '📶 Mokhaberat', 'link': '#'},
    'shatel': {'fa': '📶 شاتل', 'en': '📶 Shatel', 'link': '#'}
}

dns_public = {
    'radar': {'fa': '🛡️ رادار', 'en': '🛡️ Radar', 'link': 'https://radar.game'},
    'electro': {'fa': '⚡ الکترو', 'en': '⚡ Electro', 'link': 'https://electro.ir'},
    '403': {'fa': '🌍 403', 'en': '🌍 403', 'link': 'https://403.online'},
    'shekan': {'fa': '🔓 شکن', 'en': '🔓 Shekan', 'link': 'https://shekan.ir'}
}

wireguard_sections = {
    'vpn': {'fa': '🔐 Wire VPN', 'en': '🔐 Wire VPN'},
    'dns': {'fa': '🌐 Wire DNS', 'en': '🌐 Wire DNS'}
}

# ========== هندلر استارت (با پشتیبانی از رفرال) ==========
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    args = message.text.split()

    # بررسی رفرال
    if len(args) > 1:
        ref_param = args[1]
        if ref_param.startswith('ref'):
            try:
                referrer_id = ref_param[3:]  # حذف 'ref'
                if referrer_id != str(user_id):
                    add_referral(referrer_id, user_id)
                    get_user(user_id)["referred_by"] = referrer_id
                    save_data(db)
            except:
                pass

    # ارسال پیام پروموشن
    bot.send_message(chat_id, get_text('promotion', 'fa'))

    # درخواست انتخاب زبان
    bot.send_message(chat_id, get_text('choose_lang', 'fa'), reply_markup=language_keyboard())

# ========== هندلر کالبک ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data
    lang = get_user(user_id).get("lang", "fa")

    # ===== انتخاب زبان =====
    if data.startswith('lang_'):
        new_lang = data.split('_')[1]
        update_user(user_id, {"lang": new_lang})
        lang = new_lang

        # متن انگیزشی تصادفی
        bot.send_message(chat_id, random_motivation(lang))

        # منوی اصلی
        bot.edit_message_text(
            get_text('welcome_main', lang),
            chat_id,
            message_id,
            reply_markup=main_menu_keyboard(lang)
        )
        bot.answer_callback_query(call.id, "✅ " + ("زبان انتخاب شد" if lang == 'fa' else "Language set"))

    # ===== بررسی عضویت =====
    elif data == 'check':
        if is_member(user_id):
            bot.answer_callback_query(call.id, get_text('verified_membership', lang))
            # به‌روزرسانی شمارش رفرال‌های معرف این کاربر (اگر وجود دارد)
            referrer = get_user(user_id).get("referred_by")
            if referrer:
                add_referral(referrer, user_id)
            bot.edit_message_text(
                get_text('welcome_main', lang),
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(lang)
            )
        else:
            bot.answer_callback_query(call.id, get_text('not_member', lang), show_alert=True)

    # ===== منوی اصلی و ناوبری =====
    elif data == 'back_main':
        bot.edit_message_text(
            get_text('welcome_main', lang),
            chat_id,
            message_id,
            reply_markup=main_menu_keyboard(lang)
        )

    elif data == 'change_lang':
        bot.edit_message_text(
            get_text('choose_lang', lang),
            chat_id,
            message_id,
            reply_markup=language_keyboard()
        )

    elif data == 'channels':
        bot.answer_callback_query(call.id, get_text('channels_info', lang), show_alert=True)

    # ===== دسته‌بندی‌های اصلی =====
    elif data == 'menu_vip':
        bot.edit_message_text(
            get_text('vip_title', lang) if 'vip_title' in get_text.__defaults__ else "💎 VIP Files",
            chat_id,
            message_id,
            reply_markup=build_category_menu(vip_files, 'vip', lang)
        )

    elif data == 'menu_free':
        bot.edit_message_text(
            get_text('free_title', lang) if 'free_title' in get_text.__defaults__ else "🎁 Free Files",
            chat_id,
            message_id,
            reply_markup=build_category_menu(free_files, 'free', lang)
        )

    elif data == 'menu_gaming':
        bot.edit_message_text(
            get_text('gaming_title', lang) if 'gaming_title' in get_text.__defaults__ else "🎮 Gaming Highlights",
            chat_id,
            message_id,
            reply_markup=build_category_menu(gaming_clips, 'gaming', lang)
        )

    elif data == 'menu_dns':
        bot.edit_message_text(
            get_text('dns_title', lang) if 'dns_title' in get_text.__defaults__ else "🌐 DNS Services",
            chat_id,
            message_id,
            reply_markup=dns_main_keyboard(lang)
        )

    elif data == 'menu_wireguard':
        bot.edit_message_text(
            get_text('wireguard_title', lang) if 'wireguard_title' in get_text.__defaults__ else "🔐 Wireguard",
            chat_id,
            message_id,
            reply_markup=wireguard_main_keyboard(lang)
        )

    elif data == 'menu_codm':
        bot.edit_message_text(
            get_text('codm_title', lang) if 'codm_title' in get_text.__defaults__ else "🆓 CODM Accounts",
            chat_id,
            message_id,
            reply_markup=codm_main_keyboard(lang)
        )

    # ===== DNS اپراتورها =====
    elif data.startswith('dns_operator_'):
        op = data.replace('dns_operator_', '')
        name = dns_operators[op][lang]
        # فعلاً لینک نداریم، پیام بروزرسانی
        bot.send_message(chat_id, f"🌐 {name}\n\n" + get_text('update_message', lang))
        bot.answer_callback_query(call.id)

    # ===== DNS عمومی =====
    elif data == 'dns_public':
        text = get_text('dns_public_note', lang) + "\n\n"
        for key, val in dns_public.items():
            text += f"• {val[lang]}\n"
        text += "\n" + get_text('update_message', lang)
        bot.send_message(chat_id, text)
        bot.answer_callback_query(call.id)

    # ===== تست رایگان DNS =====
    elif data == 'dns_free':
        now = time.time()
        user_free = db["dns_free"].get(str(user_id))
        if user_free:
            activation_time = user_free
            remaining = 6*3600 - (now - activation_time)
            if remaining > 0:
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                time_str = f"{hours} ساعت {minutes} دقیقه"
                msg = get_text('dns_free_active', lang).format(time=time_str)
                bot.send_message(chat_id, msg, parse_mode='Markdown')
                bot.answer_callback_query(call.id)
                return
            else:
                # منقضی شده، پاک کن
                del db["dns_free"][str(user_id)]
                save_data(db)

        # فعال‌سازی جدید
        db["dns_free"][str(user_id)] = now
        save_data(db)
        time_str = "6 ساعت 0 دقیقه"
        msg = get_text('dns_free_active', lang).format(time=time_str)
        bot.send_message(chat_id, msg, parse_mode='Markdown')
        bot.answer_callback_query(call.id, "✅ تست رایگان فعال شد!" if lang == 'fa' else fancy_text("✅ Free test activated!"))

    # ===== وایرگارد =====
    elif data in ['wire_vpn', 'wire_dns']:
        bot.send_message(chat_id, get_text('prices_update', lang))
        bot.answer_callback_query(call.id)

    # ===== CODM =====
    elif data == 'codm_referral':
        user = get_user(user_id)
        ref_code = user["ref_code"]
        msg = get_text('referral_link', lang).format(bot=BOT_USERNAME, ref=ref_code)
        bot.send_message(chat_id, msg, parse_mode='Markdown')
        bot.answer_callback_query(call.id)

    elif data == 'codm_free':
        if not is_member(user_id):
            bot.answer_callback_query(call.id, get_text('not_member', lang), show_alert=True)
            return
        count = count_successful_referrals(user_id)
        if count >= 5:
            # بررسی قبلی دریافت نکرده باشد
            if not get_user(user_id)["claimed"].get("free_account", False):
                # TODO: در آینده اکانت واقعی
                bot.send_message(chat_id, get_text('account_credentials', lang), parse_mode='Markdown')
                update_user(user_id, {"claimed.free_account": True})
                bot.answer_callback_query(call.id, "✅ اکانت با موفقیت ارسال شد!")
            else:
                bot.send_message(chat_id, "⚠️ شما قبلاً این اکانت را دریافت کرده‌اید." if lang == 'fa' else fancy_text("⚠️ You have already claimed this account."))
                bot.answer_callback_query(call.id)
        else:
            msg = get_text('codm_free_locked', lang).format(count=count)
            bot.send_message(chat_id, msg)
            bot.answer_callback_query(call.id)

    elif data == 'codm_artery':
        if not is_member(user_id):
            bot.answer_callback_query(call.id, get_text('not_member', lang), show_alert=True)
            return
        count = count_successful_referrals(user_id)
        if count >= 10:
            if not get_user(user_id)["claimed"].get("artery", False):
                bot.send_message(chat_id, get_text('account_credentials', lang), parse_mode='Markdown')
                update_user(user_id, {"claimed.artery": True})
                bot.answer_callback_query(call.id, "✅ اکانت Artery ارسال شد!")
            else:
                bot.send_message(chat_id, "⚠️ شما قبلاً این اکانت را دریافت کرده‌اید.")
        else:
            msg = get_text('codm_artery_locked', lang).format(count=count)
            bot.send_message(chat_id, msg)

    elif data == 'codm_vivan':
        if not is_member(user_id):
            bot.answer_callback_query(call.id, get_text('not_member', lang), show_alert=True)
            return
        count = count_successful_referrals(user_id)
        if count >= 15:
            if not get_user(user_id)["claimed"].get("vivan", False):
                bot.send_message(chat_id, get_text('account_credentials', lang), parse_mode='Markdown')
                update_user(user_id, {"claimed.vivan": True})
                bot.answer_callback_query(call.id, "✅ اکانت Vivan Harris ارسال شد!")
            else:
                bot.send_message(chat_id, "⚠️ شما قبلاً این اکانت را دریافت کرده‌اید.")
        else:
            msg = get_text('codm_vivan_locked', lang).format(count=count)
            bot.send_message(chat_id, msg)

    elif data == 'codm_combo':
        if not is_member(user_id):
            bot.answer_callback_query(call.id, get_text('not_member', lang), show_alert=True)
            return
        # شرط: عضو هر دو کانال باشد
        if is_member(user_id):
            msg = get_text('codm_combo_locked', lang).format(admin=ADMIN_ID)
            bot.send_message(chat_id, msg, parse_mode='Markdown')
            bot.answer_callback_query(call.id)
        else:
            bot.answer_callback_query(call.id, get_text('not_member', lang), show_alert=True)

    # ===== ارسال فایل‌ها (همگی در حال بروزرسانی) =====
    elif data.startswith('vip_') or data.startswith('free_') or data.startswith('gaming_'):
        # همه فایل‌ها فعلاً پیام بروزرسانی
        bot.send_message(chat_id, get_text('update_message', lang))
        bot.answer_callback_query(call.id)

# ========== اجرای بات ==========
print("🚀 Bot is running with PRO features: referral, DNS test, locked CODM accounts...")
bot.polling(none_stop=True, interval=0, timeout=30)