import telebot
import os
import random
import json
import time
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import threading

# Logging setup برای دیباگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('BOT_TOKEN', '8415766472:AAEWgokNh5qAlgds-1BdmmooPh6dXBKeF9w')  # همیشه از env استفاده کن!
bot = telebot.TeleBot(TOKEN)
CHANNEL1, CHANNEL2, ADMIN_ID, BOT_USERNAME = 'Karbawzi1File', 'Karbawzi1Trust', int(os.environ.get('ADMIN_ID', 'YOUR_ADMIN_ID')), '@Karbawzi1PV'

def fancy_text(t):
    m = {'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶', 'H': '𝙷', 'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉',
         'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐', 'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗', 'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣'}
    return ''.join(m.get(c, c) for c in t)

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
    return random.choice(MOTIVATION_FA if lang == 'fa' else MOTIVATION_EN)

DATA_FILE = 'bot_data.json'
BACKUP_FILE = 'bot_data_backup.json'
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
        # Backup هر 10 دقیقه (در thread جدا)
        if time.time() % 600 < 1:  # هر 10 دقیقه
            with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Save error: {e}")

def backup_thread():
    while True:
        time.sleep(600)  # 10 دقیقه
        save_data()

threading.Thread(target=backup_thread, daemon=True).start()

def get_user(uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {
            "lang": "fa", "ref_code": f"ref{uid}", "referred_by": None, "referrals_list": [],
            "claimed": {"free_account": False, "artery": False, "vivan": False, "combo": False},
            "last_msg": None, "current_menu": "main"
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

def edit_or_send_message(uid, cid, text, reply_markup=None, msg_id=None):
    """Edit پیام قبلی اگر ممکن، وگرنه send جدید"""
    try:
        if msg_id:
            bot.edit_message_text(text, cid, msg_id, reply_markup=reply_markup, parse_mode='Markdown')
            return msg_id
    except:
        pass  # اگر edit fail شد، send جدید
    msg = bot.send_message(cid, text, reply_markup=reply_markup, parse_mode='Markdown')
    update_user(uid, {"last_msg": msg.message_id})
    return msg.message_id

def get_text(key, lang, **kwargs):
    texts = {
        'promotion': {
            'fa': "✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌\n\n🔥 karbawzi UPD\nفراتر از یه بات ساده...\nاینجا فقط بات نیست، یک گوشه از هزاران رد پای من هست.\n\n👤 ادمین: @Karbawzi1PV\n📢 کانال اول: @Karbawzi1File\n🔒 کانال دوم: @Karbawzi1Trust\n\nما موندگاریم، چون متفاوتیم.",
            'en': fancy_text("✨ KARBAWZI PREMIUM\n\n🔥 karbawzi UPD\nMore than a simple bot...\nThis is not just a bot, it's a corner of thousands of my footprints.\n\n👤 Admin: @Karbawzi1PV\n📢 Channel 1: @Karbawzi1File\n🔒 Channel 2: @Karbawzi1Trust\n\nWe stay, because we are different.")
        },
        'choose_lang': {'fa': '🌍 زبان خود را انتخاب کنید:', 'en': fancy_text('🌍 Choose your language:')},
        'welcome_main': {'fa': '✨ به پنل اصلی خوش اومدی!', 'en': fancy_text('✨ Welcome to Main Panel!')},
        'dns_free_active': {
            'fa': '✅ تست رایگان فعال\n\nپرایمری: `78.157.53.52`\nثانویه: `78.157.53.219`\n\n⏳ {time} باقی‌مانده',
            'en': fancy_text('✅ Free test active\n\nPrimary: `78.157.53.52`\nSecondary: `78.157.53.219`\n\n⏳ {time} left')
        },
        'dns_public_note': {'fa': '🌍 DNS عمومی رایگان', 'en': fancy_text('🌍 Public free DNS')},
        'referral_link': {'fa': '🔗 لینک معرفی شما:\n`https://t.me/{bot}?start={ref}`', 'en': fancy_text('🔗 Your referral link:\n`https://t.me/{bot}?start={ref}`')},
        'account_credentials': {'fa': '📋 اکانت تست\n📧 `test@gmail.com`\n🔑 `test.`', 'en': fancy_text('📋 Test account\n📧 `test@gmail.com`\n🔑 `test.`')},
        'update': {'fa': '🔄 در حال بروزرسانی', 'en': fancy_text('🔄 Updating...')},
        'vip_title': {'fa': '💎 بخش VIP', 'en': fancy_text('💎 VIP Section')},
        'free_title': {'fa': '🎁 بخش رایگان', 'en': fancy_text('🎁 Free Section')},
        'gaming_title': {'fa': '🎮 بخش گیمینگ', 'en': fancy_text('🎮 Gaming Section')},
        'dns_title': {'fa': '🌐 بخش DNS', 'en': fancy_text('🌐 DNS Section')},
        'wireguard_title': {'fa': '🔐 بخش وایرگارد', 'en': fancy_text('🔐 Wireguard Section')},
        'codm_title': {'fa': '🆓 بخش کالاف دیوتی', 'en': fancy_text('🆓 CODM Section')},
        'confirm_claim': {'fa': '✅ آیا مطمئن هستید؟', 'en': fancy_text('✅ Are you sure?')},
        'already_claimed': {'fa': '⚠️ قبلاً دریافت کردید', 'en': fancy_text('⚠️ Already claimed')},
        'need_more': {'fa': '❌ نیاز به {need} دعوت دیگر', 'en': fancy_text('❌ Need {need} more invites')},
        'join_channels': {'fa': '❌ ابتدا عضو کانال‌ها شوید', 'en': fancy_text('❌ Join channels first')},
        'stats': {'fa': '📊 آمار:\nکاربران: {users}\nریفرال‌ها: {refs}', 'en': fancy_text('📊 Stats:\nUsers: {users}\nReferrals: {refs}')}
    }
    return texts.get(key, {}).get(lang, '').format(**kwargs)

# ========== Inline Keyboards ==========
def language_keyboard(msg_id, uid):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇮🇷 فارسی", callback_data=f"lang_fa_{uid}_{msg_id}"),
        InlineKeyboardButton("🇬🇧 English", callback_data=f"lang_en_{uid}_{msg_id}")
    )
    return markup

def main_menu_keyboard(lang, uid, msg_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("💎 VIP", callback_data=f"vip_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🎁 فایل رایگان", callback_data=f"free_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🎮 گیمینگ", callback_data=f"gaming_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🌐 DNS", callback_data=f"dns_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🔐 وایرگارد", callback_data=f"wireguard_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🆓 کالاف دیوتی", callback_data=f"codm_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🌍 تغییر زبان", callback_data=f"lang_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("📢 کانال‌ها", callback_data=f"channels_{lang}_{uid}_{msg_id}")
    ]
    if lang == 'en':
        for btn in buttons:
            btn.text = fancy_text(btn.text)
    markup.add(*buttons)
    return markup

def back_button(lang, uid, msg_id, menu="main"):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 برگشت به منوی اصلی" if lang == 'fa' else fancy_text("🔙 Back to Main Menu"),
                                    callback_data=f"back_{menu}_{lang}_{uid}_{msg_id}"))
    return markup

def dns_keyboard(lang, uid, msg_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("📶 ایرانسل", callback_data=f"dns_irancell_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("📶 همراه اول", callback_data=f"dns_mci_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("📶 مخابرات", callback_data=f"dns_mokhaberat_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("📶 شاتل", callback_data=f"dns_shatel_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🌍 DNS عمومی", callback_data=f"dns_public_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🧪 تست رایگان", callback_data=f"dns_free_{lang}_{uid}_{msg_id}")
    ]
    if lang == 'en':
        for btn in buttons:
            btn.text = fancy_text(btn.text)
    markup.add(*buttons)
    markup.row(*[InlineKeyboardButton("🔙 برگشت", callback_data=f"back_dns_{lang}_{uid}_{msg_id}")])
    return markup

def wireguard_keyboard(lang, uid, msg_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("🔐 VPN", callback_data=f"wg_vpn_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🌐 DNS", callback_data=f"wg_dns_{lang}_{uid}_{msg_id}")
    ]
    if lang == 'en':
        for btn in buttons:
            btn.text = fancy_text(btn.text)
    markup.add(*buttons)
    markup.row(*[InlineKeyboardButton("🔙 برگشت", callback_data=f"back_wireguard_{lang}_{uid}_{msg_id}")])
    return markup

def category_keyboard(items, prefix, lang, uid, msg_id):
    markup = InlineKeyboardMarkup(row_width=2)
    for k, v in items.items():
        btn_text = v[lang] if lang == 'fa' else fancy_text(v[lang])
        markup.add(InlineKeyboardButton(btn_text, callback_data=f"{prefix}_{k}_{lang}_{uid}_{msg_id}"))
    markup.row(*[InlineKeyboardButton("🔙 برگشت", callback_data=f"back_{prefix}_{lang}_{uid}_{msg_id}")])
    return markup

def codm_keyboard(lang, uid, msg_id):
    markup = InlineKeyboardMarkup(row_width=1)
    is_mem = is_member(uid)
    cnt = count_successful_referrals(uid)
    status = '✅' if is_mem else '❌'
    
    free_text = f"🎮 اکانت رایگان {status} | {cnt}/5"
    artery_text = f"🔥 Artery {status} | {cnt}/10"
    vivan_text = f"✨ Vivan Harris {status} | {cnt}/15"
    
    if lang == 'en':
        free_text = fancy_text(f"🎮 Free Account {status} | {cnt}/5")
        artery_text = fancy_text(f"🔥 Artery {status} | {cnt}/10")
        vivan_text = fancy_text(f"✨ Vivan Harris {status} | {cnt}/15")
    
    buttons = [
        InlineKeyboardButton(free_text, callback_data=f"codm_free_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton(artery_text, callback_data=f"codm_artery_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton(vivan_text, callback_data=f"codm_vivan_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("📋 لیست کمبو", callback_data=f"codm_combo_{lang}_{uid}_{msg_id}"),
        InlineKeyboardButton("🔗 لینک معرفی", callback_data=f"codm_ref_{lang}_{uid}_{msg_id}")
    ]
    markup.add(*buttons)
    markup.row(*[InlineKeyboardButton("🔙 برگشت", callback_data=f"back_codm_{lang}_{uid}_{msg_id}")])
    return markup

# ========== Handlers ==========
@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    cid = m.chat.id
    args = m.text.split()
    
    # Referral check
    if len(args) > 1 and args[1].startswith('ref'):
        try:
            rid = args[1][3:]
            if rid != str(uid):
                add_referral(rid, uid)
                get_user(uid)["referred_by"] = rid
                save_data()
        except Exception as e:
            logger.error(f"Referral error: {e}")
    
    user = get_user(uid)
    lang = user.get("lang", 'fa')
    
    # Delete /start message (optional, only if possible)
    try:
        bot.delete_message(cid, m.message_id)
    except:
        pass
    
    msg_id = edit_or_send_message(uid, cid, get_text('promotion', lang), language_keyboard(None, uid))
    update_user(uid, {"last_msg": msg_id})

@bot.message_handler(commands=['stats'])
def stats(m):
    if m.from_user.id != ADMIN_ID:
        return
    users = len(db["users"])
    total_refs = sum(len(u.get("referrals_list", [])) for u in db["users"].values())
    text = get_text('stats', 'fa', users=users, refs=total_refs)  # یا lang کاربر
    bot.send_message(m.chat.id, text)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    data = call.data.split('_')
    action = data[0]
    lang = data[1] if len(data) > 1 else get_user(uid).get("lang", 'fa')
    msg_id = int(data[-1])
    
    user = get_user(uid)
    update_user(uid, {"lang": lang, "current_menu": action if action in ["codm", "dns", "wireguard"] else "main"})
    
    # Answer callback to remove loading
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    
    # Send motivation if hourly
    now = time.time()
    last = db["last_motivation"].get(str(uid), 0)
    if now - last >= 3600:
        db["last_motivation"][str(uid)] = now
        save_data()
        bot.send_message(cid, random_motivation(lang))
    
    try:
        if action == "lang":
            new_lang = data[1]  # fa or en
            update_user(uid, {"lang": new_lang})
            lang = new_lang
            edit_or_send_message(uid, cid, get_text('welcome_main', lang), main_menu_keyboard(lang, uid, msg_id), msg_id)
            return
        
        # Main menu actions
        if action in ["back", "channels"]:
            if action == "channels":
                bot.send_message(cid, f"📢 @{CHANNEL1}\n🔒 @{CHANNEL2}")
            edit_or_send_message(uid, cid, get_text('welcome_main', lang), main_menu_keyboard(lang, uid, msg_id), msg_id)
            return
        
        # VIP
        if action == "vip":
            edit_or_send_message(uid, cid, get_text('vip_title', lang), category_keyboard(vip_files, 'vip', lang, uid, msg_id), msg_id)
            return
        if action.startswith("vip_"):
            edit_or_send_message(uid, cid, get_text('update', lang), None, msg_id)
            time.sleep(1)  # Simulate loading
            edit_or_send_message(uid, cid, get_text('vip_title', lang), category_keyboard(vip_files, 'vip', lang, uid, msg_id), msg_id)
            return
        
        # Free files
        if action == "free":
            edit_or_send_message(uid, cid, get_text('free_title', lang), category_keyboard(free_files, 'free', lang, uid, msg_id), msg_id)
            return
        if action.startswith("free_"):
            edit_or_send_message(uid, cid, get_text('update', lang), None, msg_id)
            time.sleep(1)
            edit_or_send_message(uid, cid, get_text('free_title', lang), category_keyboard(free_files, 'free', lang, uid, msg_id), msg_id)
            return
        
        # Gaming
        if action == "gaming":
            edit_or_send_message(uid, cid, get_text('gaming_title', lang), category_keyboard(gaming_clips, 'gaming', lang, uid, msg_id), msg_id)
            return
        if action.startswith("gaming_"):
            edit_or_send_message(uid, cid, get_text('update', lang), None, msg_id)
            time.sleep(1)
            edit_or_send_message(uid, cid, get_text('gaming_title', lang), category_keyboard(gaming_clips, 'gaming', lang, uid, msg_id), msg_id)
            return
        
        # DNS
        if action == "dns":
            edit_or_send_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang, uid, msg_id), msg_id)
            return
        if action.startswith("dns_") and not action.startswith("dns_free_"):
            edit_or_send_message(uid, cid, get_text('update', lang), None, msg_id)
            time.sleep(1)
            edit_or_send_message(uid, cid, get_text('dns_title', lang), dns_keyboard(lang, uid, msg_id), msg_id)
            return
        if action == "dns_public":
            txt = get_text('dns_public_note', lang) + "\n" + "\n".join(f"• {v[lang]}" for v in dns_public_list.values())
            edit_or_send_message(uid, cid, txt, back_button(lang, uid, msg_id, "dns"), msg_id)
            return
        if action == "dns_free":
            now = time.time()
            uid_str = str(uid)
            if uid_str in db["dns_free"]:
                rem = 6*3600 - (now - db["dns_free"][uid_str])
                if rem > 0:
                    h = int(rem // 3600)
                    m = int((rem % 3600) // 60)
                    ts = f"{h}h {m}m" if lang == 'en' else f"{h} ساعت {m} دقیقه"
                    edit_or_send_message(uid, cid, get_text('dns_free_active', lang, time=ts), dns_keyboard(lang, uid, msg_id), msg_id)
                    return
                else:
                    del db["dns_free"][uid_str]
                    save_data()
            db["dns_free"][uid_str] = now
            save_data()
            ts = "6h 0m" if lang == 'en' else "6 ساعت 0 دقیقه"
            edit_or_send_message(uid, cid, get_text('dns_free_active', lang, time=ts), dns_keyboard(lang, uid, msg_id), msg_id)
            return
        
        # Wireguard
        if action == "wireguard":
            edit_or_send_message(uid, cid, get_text('wireguard_title', lang), wireguard_keyboard(lang, uid, msg_id), msg_id)
            return
        if action.startswith("wg_"):
            edit_or_send_message(uid, cid, get_text('update', lang), None, msg_id)
            time.sleep(1)
            edit_or_send_message(uid, cid, get_text('wireguard_title', lang), wireguard_keyboard(lang, uid, msg_id), msg_id)
            return
        
        # CODM
        if action == "codm":
            edit_or_send_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid, msg_id), msg_id)
            return
        if action.startswith("codm_"):
            if not is_member(uid):
                edit_or_send_message(uid, cid, get_text('join_channels', lang), codm_keyboard(lang, uid, msg_id), msg_id)
                return
            
            cnt = count_successful_referrals(uid)
            claim_key = None
            need = 0
            if "free" in action:
                claim_key = "free_account"
                need = 5 - cnt
            elif "artery" in action:
                claim_key = "artery"
                need = 10 - cnt
            elif "vivan" in action:
                claim_key = "vivan"
                need = 15 - cnt
            elif "combo" in action:
                bot.send_message(cid, f"👤 {ADMIN_ID}")
                edit_or_send_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid, msg_id), msg_id)
                return
            elif "ref" in action:
                ref = user["ref_code"]
                bot.send_message(cid, get_text('referral_link', lang, bot=BOT_USERNAME, ref=ref))
                edit_or_send_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid, msg_id), msg_id)
                return
            
            if need <= 0:
                if not user["claimed"][claim_key]:
                    # Confirmation
                    conf_markup = InlineKeyboardMarkup()
                    conf_markup.add(InlineKeyboardButton("✅ تأیید", callback_data=f"confirm_{claim_key}_{lang}_{uid}_{msg_id}"),
                                    InlineKeyboardButton("❌ لغو", callback_data=f"cancel_{lang}_{uid}_{msg_id}"))
                    if lang == 'en':
                        conf_markup.inline_keyboard[0][0].text = fancy_text("✅ Confirm")
                        conf_markup.inline_keyboard[0][1].text = fancy_text("❌ Cancel")
                    edit_or_send_message(uid, cid, get_text('confirm_claim', lang), conf_markup, msg_id)
                else:
                    edit_or_send_message(uid, cid, get_text('already_claimed', lang), codm_keyboard(lang, uid, msg_id), msg_id)
            else:
                edit_or_send_message(uid, cid, get_text('need_more', lang, need=need), codm_keyboard(lang, uid, msg_id), msg_id)
            return
        
        # Confirmations
        if action.startswith("confirm_"):
            claim_key = action.split('_')[1]
            if not user["claimed"][claim_key]:
                bot.send_message(cid, get_text('account_credentials', lang))
                user["claimed"][claim_key] = True
                save_data()
            edit_or_send_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid, msg_id), msg_id)
            return
        if action == "cancel":
            edit_or_send_message(uid, cid, get_text('codm_title', lang), codm_keyboard(lang, uid, msg_id), msg_id)
            return
    
    except Exception as e:
        logger.error(f"Callback error: {e}")
        bot.answer_callback_query(call.id, "خطا رخ داد! دوباره تلاش کنید." if lang == 'fa' else "Error occurred! Try again.")

@bot.message_handler(func=lambda m: True)
def handle_unknown(m):
    # Ignore non-command messages
    pass

# دیکشنری‌های محتوا (همون قبلی)
vip_files = {'promax': {'fa': '🚀 ProMax', 'en': '🚀 ProMax'}, 'topvip': {'fa': '👑 TopVIP', 'en': '👑 TopVIP'}}
free_files = {'free': {'fa': '🎁 فایل رایگان', 'en': '🎁 Free File'}}
gaming_clips = {'clip1': {'fa': '🎬 اسنیپر حرفه‌ای', 'en': '🎬 Pro Sniper'}, 'clip2': {'fa': '🔥 کلچ ۱vs۵', 'en': '🔥 1vs5 Clutch'}}
dns_public_list = {'radar': {'fa': '🛡️ رادار', 'en': '🛡️ Radar'}, 'electro': {'fa': '⚡ الکترو', 'en': '⚡ Electro'}, '403': {'fa': '🌍 403', 'en': '🌍 403'}, 'shekan': {'fa': '🔓 شکن', 'en': '🔓 Shekan'}}

print("🚀 Professional Bot is running with INLINE KEYBOARDS...")
bot.polling(none_stop=True, interval=0, timeout=30)