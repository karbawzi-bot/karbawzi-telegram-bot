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
    "「بعضی دیوارها نه برای دور نگه‌داشتن ما، بلکه برای محک زدن عزم ما ساخته شده‌اند。」 — ناشناس"
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
    "💭 \"It is not the strongest of the species that survives, nor the most intelligent, but the one most responsive to change.\" — Leon C. Megginson"
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
            'fa':"✨ 𝐊𝐀𝐑𝐁𝐀𝐖𝐙𝐈 𝐏𝐑𝐄𝐌𝐈𝐔𝐌\n\n🔥 karbawzi UPD\nفراتر از یه بات ساده...\nاینجا فقط بات نیست، یک گوشه از هزاران رد پای من هست.\n\n👤 ادمین: @Karbawzi1PV\n📢 کانال اول: @Karbawzi1File\n🔒 کانال دوم: @Karbawzi1Trust\n\nما موندگاریم، چون متفاوتیم.",
            'en':fancy_text("✨ KARBAWZI PREMIUM\n\n🔥 karbawzi UPD\nMore than a simple bot...\nThis is not just a bot, it's a corner of thousands of my footprints.\n\n👤 Admin: @Karbawzi1PV\n📢 Channel 1: @Karbawzi1File\n🔒 Channel 2: @Karbawzi1Trust\n\nWe stay, because we are different.")
        },
        'choose_lang':{'fa':'🌍 زبان خود را انتخاب کنید:', 'en':fancy_text('🌍 Choose your language:')},
        'welcome_main':{'fa':'✨ به پنل اصلی خوش اومدی!', 'en':fancy_text('✨ Welcome to Main Panel!')},
        'verified_membership':{'fa':'✅ تایید شدی!', 'en':fancy_text('✅ Verified!')},
        'not_member':{'fa':'❌ ابتدا عضو کانال‌ها شوید', 'en':fancy_text('❌ Join channels first')},
        'channels_info':{'fa':'📢 @Karbawzi1File\n🔒 @Karbawzi1Trust', 'en':fancy_text('📢 @Karbawzi1File\n🔒 @Karbawzi1Trust')},
        'dns_free_active':{'fa':'✅ تست رایگان فعال\n\nپرایمری: `78.157.53.52`\nثانویه: `78.157.53.219`\n\n⏳ {time} باقی‌مانده', 'en':fancy_text('✅ Free test active\n\nPrimary: `78.157.53.52`\nSecondary: `78.157.53.219`\n\n⏳ {time} left')},
        'dns_public_note':{'fa':'🌍 DNS عمومی رایگان', 'en':fancy_text('🌍 Public free DNS')},
        'referral_link':{'fa':'🔗 لینک معرفی شما:\n`https://t.me/{bot}?start={ref}`', 'en':fancy_text('🔗 Your referral link:\n`https://t.me/{bot}?start={ref}`')},
        'account_credentials':{'fa':'📋 اکانت تست\n📧 `test@gmail.com`\n🔑 `test.`', 'en':fancy_text('📋 Test account\n📧 `test@gmail.com`\n🔑 `test.`')},
        'already_claimed':{'fa':'⚠️ قبلاً دریافت کردید', 'en':fancy_text('⚠️ Already claimed')},
        'update':{'fa':'🔄 در حال بروزرسانی', 'en':fancy_text('🔄 Updating...')},
        'prices_update':{'fa':'💰 بروزرسانی قیمت‌ها', 'en':fancy_text('💰 Updating prices...')},
    }
    
    # متون شرطی که می‌خواهیم دکمه‌ها زیرشون باشه
    conditional = {
        'codm_free':{'fa':f'🔒 اکانت رایگان\n✅ عضو کانال‌ها: {"✓" if is_member_global else "✗"}\n👥 دعوت‌ها: {count_global}/5', 
                    'en':fancy_text(f'🔒 Free account\n✅ Joined: {"✓" if is_member_global else "✗"}\n👥 Invites: {count_global}/5')},
        'codm_artery':{'fa':f'🔒 Artery\n✅ عضو کانال‌ها: {"✓" if is_member_global else "✗"}\n👥 دعوت‌ها: {count_global}/10',
                      'en':fancy_text(f'🔒 Artery\n✅ Joined: {"✓" if is_member_global else "✗"}\n👥 Invites: {count_global}/10')},
        'codm_vivan':{'fa':f'🔒 Vivan Harris\n✅ عضو کانال‌ها: {"✓" if is_member_global else "✗"}\n👥 دعوت‌ها: {count_global}/15',
                     'en':fancy_text(f'🔒 Vivan Harris\n✅ Joined: {"✓" if is_member_global else "✗"}\n👥 Invites: {count_global}/15')},
    }
    
    if key in conditional:
        return conditional[key][lang]
    return t.get(key,{}).get(lang,t[key]['en'])

def language_keyboard():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("🇮🇷 فارسی",callback_data='lang_fa'),
          InlineKeyboardButton("🇬🇧 English",callback_data='lang_en'))
    return m

def main_menu_keyboard(lang):
    m=InlineKeyboardMarkup(row_width=2)
    if lang=='fa':
        buttons=[
            InlineKeyboardButton("💎 VIP",callback_data='menu_vip'),
            InlineKeyboardButton("🎁 رایگان",callback_data='menu_free'),
            InlineKeyboardButton("🎮 گیمینگ",callback_data='menu_gaming'),
            InlineKeyboardButton("🌐 DNS",callback_data='menu_dns'),
            InlineKeyboardButton("🔐 وایرگارد",callback_data='menu_wireguard'),
            InlineKeyboardButton("🆓 کالاف",callback_data='menu_codm'),
            InlineKeyboardButton("🌍 زبان",callback_data='change_lang'),
            InlineKeyboardButton("📢 کانال‌ها",callback_data='channels')
        ]
    else:
        buttons=[
            InlineKeyboardButton(fancy_text("💎 VIP"),callback_data='menu_vip'),
            InlineKeyboardButton(fancy_text("🎁 FREE"),callback_data='menu_free'),
            InlineKeyboardButton(fancy_text("🎮 GAMING"),callback_data='menu_gaming'),
            InlineKeyboardButton(fancy_text("🌐 DNS"),callback_data='menu_dns'),
            InlineKeyboardButton(fancy_text("🔐 WIRE"),callback_data='menu_wireguard'),
            InlineKeyboardButton(fancy_text("🆓 CODM"),callback_data='menu_codm'),
            InlineKeyboardButton(fancy_text("🌍 LANGUAGE"),callback_data='change_lang'),
            InlineKeyboardButton(fancy_text("📢 CHANNELS"),callback_data='channels')
        ]
    m.add(*buttons)
    return m

def build_category_menu(items, prefix, lang):
    m=InlineKeyboardMarkup(row_width=2)
    for k,v in items.items():
        m.add(InlineKeyboardButton(v[lang], callback_data=f'{prefix}_{k}'))
    m.add(InlineKeyboardButton("🔙 برگشت" if lang=='fa' else fancy_text("🔙 Back"), callback_data='back_main'))
    return m

def dns_keyboard(lang):
    m=InlineKeyboardMarkup(row_width=2)
    if lang=='fa':
        m.add(InlineKeyboardButton("📶 ایرانسل", callback_data='dns_operator_irancell'),
              InlineKeyboardButton("📶 همراه اول", callback_data='dns_operator_mci'))
        m.add(InlineKeyboardButton("📶 مخابرات", callback_data='dns_operator_mokhaberat'),
              InlineKeyboardButton("📶 شاتل", callback_data='dns_operator_shatel'))
        m.add(InlineKeyboardButton("🌍 عمومی", callback_data='dns_public'),
              InlineKeyboardButton("🧪 تست رایگان", callback_data='dns_free'))
    else:
        m.add(InlineKeyboardButton(fancy_text("📶 Irancell"), callback_data='dns_operator_irancell'),
              InlineKeyboardButton(fancy_text("📶 MCI"), callback_data='dns_operator_mci'))
        m.add(InlineKeyboardButton(fancy_text("📶 Mokhaberat"), callback_data='dns_operator_mokhaberat'),
              InlineKeyboardButton(fancy_text("📶 Shatel"), callback_data='dns_operator_shatel'))
        m.add(InlineKeyboardButton(fancy_text("🌍 Public"), callback_data='dns_public'),
              InlineKeyboardButton(fancy_text("🧪 Free Test"), callback_data='dns_free'))
    m.add(InlineKeyboardButton("🔙 برگشت" if lang=='fa' else fancy_text("🔙 Back"), callback_data='back_main'))
    return m

def wireguard_keyboard(lang):
    m=InlineKeyboardMarkup(row_width=2)
    if lang=='fa':
        m.add(InlineKeyboardButton("🔐 VPN", callback_data='wire_vpn'),
              InlineKeyboardButton("🌐 DNS", callback_data='wire_dns'))
    else:
        m.add(InlineKeyboardButton(fancy_text("🔐 VPN"), callback_data='wire_vpn'),
              InlineKeyboardButton(fancy_text("🌐 DNS"), callback_data='wire_dns'))
    m.add(InlineKeyboardButton("🔙 برگشت" if lang=='fa' else fancy_text("🔙 Back"), callback_data='back_main'))
    return m

def codm_keyboard(lang, uid):
    is_mem = is_member(uid)
    cnt = count_successful_referrals(uid)
    
    m=InlineKeyboardMarkup(row_width=1)
    
    if lang=='fa':
        free_text = f"🎮 اکانت رایگان {'✓' if is_mem else '✗'} | {cnt}/5"
        artery_text = f"🔥 Artery {'✓' if is_mem else '✗'} | {cnt}/10"
        vivan_text = f"✨ Vivan Harris {'✓' if is_mem else '✗'} | {cnt}/15"
        
        m.add(InlineKeyboardButton(free_text, callback_data='codm_free'))
        m.add(InlineKeyboardButton(artery_text, callback_data='codm_artery'))
        m.add(InlineKeyboardButton(vivan_text, callback_data='codm_vivan'))
        m.add(InlineKeyboardButton("📋 لیست کمبو", callback_data='codm_combo'),
              InlineKeyboardButton("🔗 لینک معرفی", callback_data='codm_referral'))
    else:
        free_text = fancy_text(f"🎮 Free Account {'✓' if is_mem else '✗'} | {cnt}/5")
        artery_text = fancy_text(f"🔥 Artery {'✓' if is_mem else '✗'} | {cnt}/10")
        vivan_text = fancy_text(f"✨ Vivan Harris {'✓' if is_mem else '✗'} | {cnt}/15")
        
        m.add(InlineKeyboardButton(free_text, callback_data='codm_free'))
        m.add(InlineKeyboardButton(artery_text, callback_data='codm_artery'))
        m.add(InlineKeyboardButton(vivan_text, callback_data='codm_vivan'))
        m.add(InlineKeyboardButton(fancy_text("📋 Combo List"), callback_data='codm_combo'),
              InlineKeyboardButton(fancy_text("🔗 Referral Link"), callback_data='codm_referral'))
    
    m.add(InlineKeyboardButton("🔙 برگشت" if lang=='fa' else fancy_text("🔙 Back"), callback_data='back_main'))
    return m

# دیکشنری‌های منوها
vip_files={'promax':{'fa':'🚀 ProMax','en':'🚀 ProMax'},
           'topvip':{'fa':'👑 TopVIP','en':'👑 TopVIP'}}
free_files={'free':{'fa':'🎁 فایل رایگان','en':'🎁 Free File'}}
gaming_clips={'clip1':{'fa':'🎬 اسنیپر','en':'🎬 Sniper'},
              'clip2':{'fa':'🔥 کلچ','en':'🔥 Clutch'}}
dns_public={'radar':{'fa':'🛡️ رادار','en':'🛡️ Radar'},
            'electro':{'fa':'⚡ الکترو','en':'⚡ Electro'}}

@bot.message_handler(commands=['start'])
def start(m):
    uid=m.from_user.id
    cid=m.chat.id
    args=m.text.split()
    
    if len(args)>1 and args[1].startswith('ref'):
        try:
            rid=args[1][3:]
            if rid!=str(uid):
                add_referral(rid,uid)
                get_user(uid)["referred_by"]=rid
                save_data()
        except: pass
    
    # پاک کردن پیام‌های قبلی کاربر
    try:
        bot.delete_message(cid, m.message_id)
    except: pass
    
    msg = bot.send_message(cid, get_text('promotion','fa'), reply_markup=language_keyboard())
    # ذخیره آخرین پیام برای پاک کردن بعدی
    db["users"][str(uid)]["last_msg"] = msg.message_id
    save_data()

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    uid=call.from_user.id
    cid=call.message.chat.id
    mid=call.message.message_id
    data=call.data
    lang=get_user(uid).get("lang",'fa')
    
    # پاک کردن پیام قبلی
    try:
        bot.delete_message(cid, mid)
    except: pass
    
    if data.startswith('lang_'):
        new_lang=data.split('_')[1]
        update_user(uid,{"lang":new_lang})
        lang=new_lang
        
        # متن انگیزشی
        now=time.time()
        last=db["last_motivation"].get(str(uid),0)
        if now-last>=3600:
            db["last_motivation"][str(uid)]=now
            save_data()
            bot.send_message(cid, random_motivation(lang))
        
        msg = bot.send_message(cid, get_text('welcome_main',lang), reply_markup=main_menu_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='back_main':
        msg = bot.send_message(cid, get_text('welcome_main',lang), reply_markup=main_menu_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='change_lang':
        msg = bot.send_message(cid, get_text('choose_lang',lang), reply_markup=language_keyboard())
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='channels':
        bot.answer_callback_query(call.id, get_text('channels_info',lang), show_alert=True)
        # برگشت به منوی اصلی بعد از نمایش
        msg = bot.send_message(cid, get_text('welcome_main',lang), reply_markup=main_menu_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        
    elif data=='menu_vip':
        msg = bot.send_message(cid, "💎", reply_markup=build_category_menu(vip_files,'vip',lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='menu_free':
        msg = bot.send_message(cid, "🎁", reply_markup=build_category_menu(free_files,'free',lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='menu_gaming':
        msg = bot.send_message(cid, "🎮", reply_markup=build_category_menu(gaming_clips,'gaming',lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='menu_dns':
        msg = bot.send_message(cid, "🌐", reply_markup=dns_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='menu_wireguard':
        msg = bot.send_message(cid, "🔐", reply_markup=wireguard_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='menu_codm':
        msg = bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data.startswith('dns_operator_'):
        bot.send_message(cid, get_text('update',lang))
        # برگشت به منوی DNS
        msg = bot.send_message(cid, "🌐", reply_markup=dns_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='dns_public':
        txt = get_text('dns_public_note',lang) + "\n" + "\n".join(f"• {v[lang]}" for v in dns_public.values())
        bot.send_message(cid, txt)
        msg = bot.send_message(cid, "🌐", reply_markup=dns_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='dns_free':
        now=time.time()
        uid_str=str(uid)
        if uid_str in db["dns_free"]:
            rem=6*3600-(now-db["dns_free"][uid_str])
            if rem>0:
                h=int(rem//3600)
                m=int((rem%3600)//60)
                ts = f"{h}h {m}m" if lang=='en' else f"{h} ساعت {m} دقیقه"
                bot.send_message(cid, get_text('dns_free_active',lang).format(time=ts), parse_mode='Markdown')
                msg = bot.send_message(cid, "🌐", reply_markup=dns_keyboard(lang))
                db["users"][str(uid)]["last_msg"] = msg.message_id
                save_data()
                bot.answer_callback_query(call.id)
                return
            else:
                del db["dns_free"][uid_str]
                save_data()
        
        db["dns_free"][uid_str]=now
        save_data()
        ts = "6h 0m" if lang=='en' else "6 ساعت 0 دقیقه"
        bot.send_message(cid, get_text('dns_free_active',lang).format(time=ts), parse_mode='Markdown')
        msg = bot.send_message(cid, "🌐", reply_markup=dns_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id, "✅ فعال شد!" if lang=='fa' else "✅ Activated!")
        
    elif data in ['wire_vpn', 'wire_dns']:
        bot.send_message(cid, get_text('prices_update',lang))
        msg = bot.send_message(cid, "🔐", reply_markup=wireguard_keyboard(lang))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data=='codm_referral':
        u=get_user(uid)
        bot.send_message(cid, get_text('referral_link',lang).format(bot=BOT_USERNAME, ref=u["ref_code"]), parse_mode='Markdown')
        msg = bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)
        
    elif data in ['codm_free', 'codm_artery', 'codm_vivan']:
        if not is_member(uid):
            bot.answer_callback_query(call.id, get_text('not_member',lang), show_alert=True)
            # برگشت به منوی کالاف
            msg = bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
            db["users"][str(uid)]["last_msg"] = msg.message_id
            save_data()
            return
            
        cnt = count_successful_referrals(uid)
        required = {'codm_free':5, 'codm_artery':10, 'codm_vivan':15}
        claim_key = {'codm_free':'free_account', 'codm_artery':'artery', 'codm_vivan':'vivan'}
        
        if cnt >= required[data]:
            if not get_user(uid)["claimed"][claim_key[data]]:
                bot.send_message(cid, get_text('account_credentials',lang), parse_mode='Markdown')
                db["users"][str(uid)]["claimed"][claim_key[data]] = True
                save_data()
                bot.answer_callback_query(call.id, "✅ ارسال شد!" if lang=='fa' else "✅ Sent!")
            else:
                bot.send_message(cid, get_text('already_claimed',lang))
                bot.answer_callback_query(call.id)
        else:
            bot.answer_callback_query(call.id, f"نیاز به {required[data]} دعوت" if lang=='fa' else f"Need {required[data]} invites", show_alert=True)
        
        # برگشت به منوی کالاف
        msg = bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        
    elif data=='codm_combo':
        if not is_member(uid):
            bot.answer_callback_query(call.id, get_text('not_member',lang), show_alert=True)
        else:
            bot.send_message(cid, f"👤 {ADMIN_ID}")
            bot.answer_callback_query(call.id)
        
        msg = bot.send_message(cid, "🆓", reply_markup=codm_keyboard(lang, uid))
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        
    elif data.startswith(('vip_', 'free_', 'gaming_')):
        bot.send_message(cid, get_text('update',lang))
        # برگشت به منوی مربوطه
        if data.startswith('vip_'):
            msg = bot.send_message(cid, "💎", reply_markup=build_category_menu(vip_files,'vip',lang))
        elif data.startswith('free_'):
            msg = bot.send_message(cid, "🎁", reply_markup=build_category_menu(free_files,'free',lang))
        else:
            msg = bot.send_message(cid, "🎮", reply_markup=build_category_menu(gaming_clips,'gaming',lang))
        
        db["users"][str(uid)]["last_msg"] = msg.message_id
        save_data()
        bot.answer_callback_query(call.id)

print("🚀 Bot is running...")
bot.polling(none_stop=True, interval=0, timeout=30)