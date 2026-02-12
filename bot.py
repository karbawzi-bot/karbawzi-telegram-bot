import telebot, os, random, json, time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
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

def get_text(key,lang):
    t={
        'promotion':{
            'fa':"\n━━━━━━━━━━━━━━━━━━━━\n✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐁𝐎𝐓 ✨\n━━━━━━━━━━━━━━━━━━━━\n\n🔥 فراتر از یه بات ساده...\nاینجا فقط دانلود نیست، تجربه‌ست.\n\n👤 ادمین: @Karbawzi1PV\n📢 کانال فایل‌ها: @Karbawzi1File\n🔒 کانال اعتماد: @Karbawzi1Trust\n\n━━━━━━━━━━━━━━━━━━━━\nما موندگاریم، چون متفاوتیم.\n━━━━━━━━━━━━━━━━━━━━\n",
            'en':fancy_text("\n━━━━━━━━━━━━━━━━━━━━\n✨ KARBAWZI PREMIUM BOT ✨\n━━━━━━━━━━━━━━━━━━━━\n\n🔥 More than a simple bot...\nThis is not just download, it's an experience.\n\n👤 Admin: @Karbawzi1PV\n📢 Files Channel: @Karbawzi1File\n🔒 Trust Channel: @Karbawzi1Trust\n\n━━━━━━━━━━━━━━━━━━━━\nWe stay, because we are different.\n━━━━━━━━━━━━━━━━━━━━\n")
        },
        'choose_lang':{'fa':"🌍 لطفاً زبان خود را انتخاب کنید:",'en':fancy_text("🌍 Please choose your language:")},
        'welcome_main':{'fa':"✨ به پنل اصلی خوش اومدی!\nیکی از دسته‌بندی‌های زیر رو انتخاب کن:",'en':fancy_text("✨ Welcome to Main Panel!\nChoose one of the categories below:")},
        'verified_membership':{'fa':"✅ تایید شدی! حالا به جمع حرفه‌ای‌ها خوش اومدی 🔥",'en':fancy_text("✅ Verified! Now welcome to the pros 🔥")},
        'not_member':{'fa':"❌ شما هنوز عضو کانال‌ها نشده‌اید!",'en':fancy_text("❌ You are not a member yet!")},
        'error':{'fa':"❌ خطا در ارسال فایل!",'en':fancy_text("❌ Error sending file!")},
        'channels_info':{'fa':"📢 @Karbawzi1File\n🔒 @Karbawzi1Trust",'en':fancy_text("📢 @Karbawzi1File\n🔒 @Karbawzi1Trust")},
        'update_message':{'fa':"🔄 در حال بروزرسانی بات هستیم.\nلطفاً شکیبا باشید و بعداً مراجعه کنید 🙏",'en':fancy_text("🔄 Bot is being updated.\nPlease be patient and check back later 🙏")},
        'prices_update':{'fa':"💰 قیمت‌ها در حال بروزرسانی می‌باشد.\nبه‌زودی با پیشنهادهای ویژه بازخواهیم گشت ✨",'en':fancy_text("💰 Prices are being updated.\nWe'll be back soon with special offers ✨")},
        'dns_free_active':{'fa':"✅ تست رایگان شما فعال است.\n\nپرایمری DNS: `78.157.53.52`\nثانویه DNS: `78.157.53.219`\n\n⏳ زمان باقی‌مانده: {time}\n\nپس از اتمام، می‌توانید مجدداً فعال کنید.",'en':fancy_text("✅ Your free test is active.\n\nPrimary DNS: `78.157.53.52`\nSecondary DNS: `78.157.53.219`\n\n⏳ Time left: {time}\n\nAfter expiration, you can activate again.")},
        'dns_public_note':{'fa':"🌍 DNS عمومی و کاملاً رایگان – مناسب برای دور زدن محدودیت‌های ساده",'en':fancy_text("🌍 Public & completely free DNS – suitable for bypassing simple restrictions")},
        'codm_free_locked':{'fa':"🔒 برای دریافت اکانت رایگان باید:\n✅ عضو هر دو کانال شوید\n✅ ۵ نفر را با لینک معرفی خود دعوت کنید (دعوت‌شدگان نیز عضو کانال‌ها شوند)\n\nتعداد دعوت‌های موفق فعلی: {count}/5",'en':fancy_text("🔒 To get a free account:\n✅ Join both channels\n✅ Invite 5 people via your referral link (they must also join channels)\n\nCurrent successful invites: {count}/5")},
        'codm_artery_locked':{'fa':"🔒 برای دریافت اکانت Artery (هند، تک‌سیو) باید:\n✅ عضو هر دو کانال شوید\n✅ ۱۰ نفر را با لینک معرفی دعوت کنید\n\nتعداد دعوت‌های موفق فعلی: {count}/10",'en':fancy_text("🔒 To get an Artery account (India, single save):\n✅ Join both channels\n✅ Invite 10 people via your referral link\n\nCurrent successful invites: {count}/10")},
        'codm_vivan_locked':{'fa':"🔒 برای دریافت اکانت Vivan Harris (هند، تک‌سیو) باید:\n✅ عضو هر دو کانال شوید\n✅ ۱۵ نفر را با لینک معرفی دعوت کنید\n\nتعداد دعوت‌های موفق فعلی: {count}/15",'en':fancy_text("🔒 To get a Vivan Harris account (India, single save):\n✅ Join both channels\n✅ Invite 15 people via your referral link\n\nCurrent successful invites: {count}/15")},
        'codm_combo_locked':{'fa':"🔒 برای دریافت لیست کمبو باید عضو هر دو کانال باشید.\nپس از عضویت، با ادمین زیر هماهنگ کنید:\n👤 {admin}",'en':fancy_text("🔒 To get the combo list you must be a member of both channels.\nAfter joining, contact the admin:\n👤 {admin}")},
        'account_credentials':{'fa':"📋 اکانت شما:\n📧 Gmail: `test@gmail.com`\n🔑 Password: `test.`\n\n⚠️ این اکانت صرفاً برای تست می‌باشد و در آپدیت بعدی با اکانت واقعی جایگزین خواهد شد.",'en':fancy_text("📋 Your account:\n📧 Gmail: `test@gmail.com`\n🔑 Password: `test.`\n\n⚠️ This account is for testing only and will be replaced with real accounts in the next update.")},
        'referral_link':{'fa':"🔗 لینک معرفی اختصاصی شما:\n`https://t.me/{bot}?start={ref}`\n\nاین لینک را برای دوستانتان بفرستید. هر نفر که عضو هر دو کانال شود، یک دعوت موفق برای شما حساب می‌شود.",'en':fancy_text("🔗 Your personal referral link:\n`https://t.me/{bot}?start={ref}`\n\nShare this link with your friends. Each person who joins both channels counts as a successful referral.")},
        'vip_title':{'fa':"💎 بخش فایل‌های ویژه",'en':fancy_text("💎 VIP Files Section")},
        'free_title':{'fa':"🎁 بخش فایل‌های رایگان",'en':fancy_text("🎁 Free Files Section")},
        'gaming_title':{'fa':"🎮 هایلایت گیم‌پلی",'en':fancy_text("🎮 Gaming Highlights")},
        'dns_title':{'fa':"🌐 سرویس‌های DNS",'en':fancy_text("🌐 DNS Services")},
        'wireguard_title':{'fa':"🔐 وایرگارد",'en':fancy_text("🔐 Wireguard")},
        'codm_title':{'fa':"🆓 اکانت‌های کالاف دیوتی",'en':fancy_text("🆓 CODM Accounts")},
    }
    return t.get(key,{}).get(lang,t[key]['en'])

def language_keyboard():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("🇮🇷 فارسی",callback_data='lang_fa'),InlineKeyboardButton("🇬🇧 English",callback_data='lang_en'))
    return m
def main_menu_keyboard(lang):
    m=InlineKeyboardMarkup(row_width=2)
    if lang=='fa': b=[InlineKeyboardButton("💎 VIP",callback_data='menu_vip'),InlineKeyboardButton("🎁 فایل رایگان",callback_data='menu_free'),InlineKeyboardButton("🎮 GAMING",callback_data='menu_gaming'),InlineKeyboardButton("🌐 DNS",callback_data='menu_dns'),InlineKeyboardButton("🔐 WIRE",callback_data='menu_wireguard'),InlineKeyboardButton("🆓 CODM",callback_data='menu_codm'),InlineKeyboardButton("🌍 زبان",callback_data='change_lang'),InlineKeyboardButton("📢 کانال‌ها",callback_data='channels')]
    else: b=[InlineKeyboardButton(fancy_text("💎 VIP"),callback_data='menu_vip'),InlineKeyboardButton(fancy_text("🎁 FREE"),callback_data='menu_free'),InlineKeyboardButton(fancy_text("🎮 GAMING"),callback_data='menu_gaming'),InlineKeyboardButton(fancy_text("🌐 DNS"),callback_data='menu_dns'),InlineKeyboardButton(fancy_text("🔐 WIRE"),callback_data='menu_wireguard'),InlineKeyboardButton(fancy_text("🆓 CODM"),callback_data='menu_codm'),InlineKeyboardButton(fancy_text("🌍 LANGUAGE"),callback_data='change_lang'),InlineKeyboardButton(fancy_text("📢 CHANNELS"),callback_data='channels')]
    m.add(*b); return m
def build_category_menu(cd,cp,lang):
    m=InlineKeyboardMarkup(row_width=2)
    for k,v in cd.items():
        n=v[lang]
        if lang=='en': n=fancy_text(n)
        m.add(InlineKeyboardButton(n,callback_data=f'{cp}_{k}'))
    m.add(InlineKeyboardButton("🔙 برگشت" if lang=='fa' else fancy_text("🔙 Back"),callback_data='back_main'))
    return m
def dns_main_keyboard(lang):
    m=InlineKeyboardMarkup(row_width=2)
    if lang=='fa': b=[InlineKeyboardButton("📶 ایرانسل (MTN)",callback_data='dns_operator_irancell'),InlineKeyboardButton("📶 همراه اول (MCI)",callback_data='dns_operator_mci'),InlineKeyboardButton("📶 مخابرات",callback_data='dns_operator_mokhaberat'),InlineKeyboardButton("📶 شاتل",callback_data='dns_operator_shatel'),InlineKeyboardButton("🌍 DNS عمومی",callback_data='dns_public'),InlineKeyboardButton("🧪 تست رایگان",callback_data='dns_free')]
    else: b=[InlineKeyboardButton(fancy_text("📶 Irancell (MTN)"),callback_data='dns_operator_irancell'),InlineKeyboardButton(fancy_text("📶 Hamrah Aval (MCI)"),callback_data='dns_operator_mci'),InlineKeyboardButton(fancy_text("📶 Mokhaberat"),callback_data='dns_operator_mokhaberat'),InlineKeyboardButton(fancy_text("📶 Shatel"),callback_data='dns_operator_shatel'),InlineKeyboardButton(fancy_text("🌍 Public DNS"),callback_data='dns_public'),InlineKeyboardButton(fancy_text("🧪 Free Test"),callback_data='dns_free')]
    m.add(*b)
    m.add(InlineKeyboardButton("🔙 برگشت" if lang=='fa' else fancy_text("🔙 Back"),callback_data='back_main'))
    return m
def wireguard_main_keyboard(lang):
    m=InlineKeyboardMarkup(row_width=2)
    if lang=='fa': b=[InlineKeyboardButton("🔐 Wire VPN",callback_data='wire_vpn'),InlineKeyboardButton("🌐 Wire DNS",callback_data='wire_dns')]
    else: b=[InlineKeyboardButton(fancy_text("🔐 Wire VPN"),callback_data='wire_vpn'),InlineKeyboardButton(fancy_text("🌐 Wire DNS"),callback_data='wire_dns')]
    m.add(*b)
    m.add(InlineKeyboardButton("🔙 برگشت" if lang=='fa' else fancy_text("🔙 Back"),callback_data='back_main'))
    return m
def codm_main_keyboard(lang):
    m=InlineKeyboardMarkup(row_width=2)
    if lang=='fa': b=[InlineKeyboardButton("🎮 اکانت رایگان",callback_data='codm_free'),InlineKeyboardButton("🔥 Artery",callback_data='codm_artery'),InlineKeyboardButton("✨ Vivan Harris",callback_data='codm_vivan'),InlineKeyboardButton("📋 لیست کمبو",callback_data='codm_combo'),InlineKeyboardButton("🔗 لینک معرفی",callback_data='codm_referral')]
    else: b=[InlineKeyboardButton(fancy_text("🎮 Free Account"),callback_data='codm_free'),InlineKeyboardButton(fancy_text("🔥 Artery"),callback_data='codm_artery'),InlineKeyboardButton(fancy_text("✨ Vivan Harris"),callback_data='codm_vivan'),InlineKeyboardButton(fancy_text("📋 Combo List"),callback_data='codm_combo'),InlineKeyboardButton(fancy_text("🔗 Referral Link"),callback_data='codm_referral')]
    m.add(*b)
    m.add(InlineKeyboardButton("🔙 برگشت" if lang=='fa' else fancy_text("🔙 Back"),callback_data='back_main'))
    return m

vip_files={'promax':{'fa':'🚀 ProMax','en':'🚀 ProMax'},'topvip':{'fa':'👑 TopVIP','en':'👑 TopVIP'},'youtuber':{'fa':'🎬 YouTuber','en':'🎬 YouTuber'},'fixlag':{'fa':'⚡ FixLag (ضد لگ)','en':'⚡ FixLag'}}
free_files={'free':{'fa':'🎁 فایل رایگان','en':'🎁 Free File'}}
gaming_clips={'clip1':{'fa':'🎬 اسنیپر حرفه‌ای','en':'🎬 Pro Sniper'},'clip2':{'fa':'🔥 کلچ ۱vs۵','en':'🔥 1vs5 Clutch'},'clip3':{'fa':'🏆 تورنمنت هفته','en':'🏆 Weekly Tourney'},'clip4':{'fa':'📺 آموزش حرکات','en':'📺 Movement Tips'}}
dns_operators={'irancell':{'fa':'📶 ایرانسل (MTN)','en':'📶 Irancell (MTN)'},'mci':{'fa':'📶 همراه اول (MCI)','en':'📶 Hamrah Aval (MCI)'},'mokhaberat':{'fa':'📶 مخابرات','en':'📶 Mokhaberat'},'shatel':{'fa':'📶 شاتل','en':'📶 Shatel'}}
dns_public={'radar':{'fa':'🛡️ رادار','en':'🛡️ Radar'},'electro':{'fa':'⚡ الکترو','en':'⚡ Electro'},'403':{'fa':'🌍 403','en':'🌍 403'},'shekan':{'fa':'🔓 شکن','en':'🔓 Shekan'}}
wireguard_sections={'vpn':{'fa':'🔐 Wire VPN','en':'🔐 Wire VPN'},'dns':{'fa':'🌐 Wire DNS','en':'🌐 Wire DNS'}}

@bot.message_handler(commands=['start'])
def start(m):
    uid=m.from_user.id; cid=m.chat.id; args=m.text.split()
    if len(args)>1 and args[1].startswith('ref'):
        try:
            rid=args[1][3:]
            if rid!=str(uid): add_referral(rid,uid); get_user(uid)["referred_by"]=rid; save_data()
        except: pass
    bot.send_message(cid,get_text('promotion','fa'))
    bot.send_message(cid,get_text('choose_lang','fa'),reply_markup=language_keyboard())

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    uid=call.from_user.id; cid=call.message.chat.id; mid=call.message.message_id; data=call.data
    lang=get_user(uid).get("lang",'fa')
    if data.startswith('lang_'):
        new_lang=data.split('_')[1]; update_user(uid,{"lang":new_lang}); lang=new_lang
        now=time.time(); last=db["last_motivation"].get(str(uid),0)
        if now-last>=3600:
            db["last_motivation"][str(uid)]=now; save_data()
            bot.send_message(cid,random_motivation(lang))
        bot.edit_message_text(get_text('welcome_main',lang),cid,mid,reply_markup=main_menu_keyboard(lang))
        bot.answer_callback_query(call.id,"✅ "+("زبان انتخاب شد" if lang=='fa' else "Language set"))
    elif data=='check':
        if is_member(uid):
            bot.answer_callback_query(call.id,get_text('verified_membership',lang))
            if get_user(uid).get("referred_by"): add_referral(get_user(uid)["referred_by"],uid)
            bot.edit_message_text(get_text('welcome_main',lang),cid,mid,reply_markup=main_menu_keyboard(lang))
        else: bot.answer_callback_query(call.id,get_text('not_member',lang),show_alert=True)
    elif data=='back_main':
        bot.edit_message_text(get_text('welcome_main',lang),cid,mid,reply_markup=main_menu_keyboard(lang))
    elif data=='change_lang':
        bot.edit_message_text(get_text('choose_lang',lang),cid,mid,reply_markup=language_keyboard())
    elif data=='channels':
        bot.answer_callback_query(call.id,get_text('channels_info',lang),show_alert=True)
    elif data=='menu_vip':
        bot.edit_message_text(get_text('vip_title',lang),cid,mid,reply_markup=build_category_menu(vip_files,'vip',lang))
    elif data=='menu_free':
        bot.edit_message_text(get_text('free_title',lang),cid,mid,reply_markup=build_category_menu(free_files,'free',lang))
    elif data=='menu_gaming':
        bot.edit_message_text(get_text('gaming_title',lang),cid,mid,reply_markup=build_category_menu(gaming_clips,'gaming',lang))
    elif data=='menu_dns':
        bot.edit_message_text(get_text('dns_title',lang),cid,mid,reply_markup=dns_main_keyboard(lang))
    elif data=='menu_wireguard':
        bot.edit_message_text(get_text('wireguard_title',lang),cid,mid,reply_markup=wireguard_main_keyboard(lang))
    elif data=='menu_codm':
        bot.edit_message_text(get_text('codm_title',lang),cid,mid,reply_markup=codm_main_keyboard(lang))
    elif data.startswith('dns_operator_'):
        op=data.replace('dns_operator_',''); name=dns_operators[op][lang]
        bot.send_message(cid,f"🌐 {name}\n\n"+get_text('update_message',lang)); bot.answer_callback_query(call.id)
    elif data=='dns_public':
        txt=get_text('dns_public_note',lang)+"\n\n"+("\n".join(f"• {v[lang]}" for v in dns_public.values()))+"\n\n"+get_text('update_message',lang)
        bot.send_message(cid,txt); bot.answer_callback_query(call.id)
    elif data=='dns_free':
        now=time.time(); uid_str=str(uid)
        if uid_str in db["dns_free"]:
            rem=6*3600-(now-db["dns_free"][uid_str])
            if rem>0:
                h=int(rem//3600); m=int((rem%3600)//60); ts=f"{h} ساعت {m} دقیقه"
                bot.send_message(cid,get_text('dns_free_active',lang).format(time=ts),parse_mode='Markdown')
                bot.answer_callback_query(call.id); return
            else: del db["dns_free"][uid_str]; save_data()
        db["dns_free"][uid_str]=now; save_data()
        bot.send_message(cid,get_text('dns_free_active',lang).format(time="6 ساعت 0 دقیقه"),parse_mode='Markdown')
        bot.answer_callback_query(call.id,"✅ تست رایگان فعال شد!" if lang=='fa' else fancy_text("✅ Free test activated!"))
    elif data in ['wire_vpn','wire_dns']:
        bot.send_message(cid,get_text('prices_update',lang)); bot.answer_callback_query(call.id)
    elif data=='codm_referral':
        u=get_user(uid); bot.send_message(cid,get_text('referral_link',lang).format(bot=BOT_USERNAME,ref=u["ref_code"]),parse_mode='Markdown')
        bot.answer_callback_query(call.id)
    elif data=='codm_free':
        if not is_member(uid): bot.answer_callback_query(call.id,get_text('not_member',lang),show_alert=True); return
        cnt=count_successful_referrals(uid)
        if cnt>=5:
            if not get_user(uid)["claimed"]["free_account"]:
                bot.send_message(cid,get_text('account_credentials',lang),parse_mode='Markdown')
                db["users"][str(uid)]["claimed"]["free_account"]=True; save_data()
                bot.answer_callback_query(call.id,"✅ اکانت با موفقیت ارسال شد!")
            else: bot.send_message(cid,"⚠️ شما قبلاً این اکانت را دریافت کرده‌اید." if lang=='fa' else fancy_text("⚠️ You have already claimed this account."))
        else: bot.send_message(cid,get_text('codm_free_locked',lang).format(count=cnt))
    elif data=='codm_artery':
        if not is_member(uid): bot.answer_callback_query(call.id,get_text('not_member',lang),show_alert=True); return
        cnt=count_successful_referrals(uid)
        if cnt>=10:
            if not get_user(uid)["claimed"]["artery"]:
                bot.send_message(cid,get_text('account_credentials',lang),parse_mode='Markdown')
                db["users"][str(uid)]["claimed"]["artery"]=True; save_data()
                bot.answer_callback_query(call.id,"✅ اکانت Artery ارسال شد!")
            else: bot.send_message(cid,"⚠️ شما قبلاً این اکانت را دریافت کرده‌اید.")
        else: bot.send_message(cid,get_text('codm_artery_locked',lang).format(count=cnt))
    elif data=='codm_vivan':
        if not is_member(uid): bot.answer_callback_query(call.id,get_text('not_member',lang),show_alert=True); return
        cnt=count_successful_referrals(uid)
        if cnt>=15:
            if not get_user(uid)["claimed"]["vivan"]:
                bot.send_message(cid,get_text('account_credentials',lang),parse_mode='Markdown')
                db["users"][str(uid)]["claimed"]["vivan"]=True; save_data()
                bot.answer_callback_query(call.id,"✅ اکانت Vivan Harris ارسال شد!")
            else: bot.send_message(cid,"⚠️ شما قبلاً این اکانت را دریافت کرده‌اید.")
        else: bot.send_message(cid,get_text('codm_vivan_locked',lang).format(count=cnt))
    elif data=='codm_combo':
        if not is_member(uid): bot.answer_callback_query(call.id,get_text('not_member',lang),show_alert=True); return
        if is_member(uid):
            bot.send_message(cid,get_text('codm_combo_locked',lang).format(admin=ADMIN_ID),parse_mode='Markdown')
            bot.answer_callback_query(call.id)
        else: bot.answer_callback_query(call.id,get_text('not_member',lang),show_alert=True)
    elif data.startswith('vip_') or data.startswith('free_') or data.startswith('gaming_'):
        bot.send_message(cid,get_text('update_message',lang)); bot.answer_callback_query(call.id)

print("🚀 Bot is running with ULTRA PREMIUM features...")
bot.polling(none_stop=True, interval=0, timeout=30)