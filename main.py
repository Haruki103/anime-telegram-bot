import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Log sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token
TOKEN = os.getenv('BOT_TOKEN', '8507552194:AAE9L2rlr2dg4ngv_gKImaQAypIohdktInI')

# Anime ma'lumotlari
ANIMES = {
    1: {
        "name": "Iblislar hukmdori ishda!",
        "episodes": 13,
        "country": "Yaponiya",
        "language": "O'zbek tilida",
        "year": 2025,
        "genre": "Fantastik, Ekshn",
        "link": "https://t.me/Haruki_animelaruzboty/1"
    },
    2: {
        "name": "Naruto",
        "episodes": 220,
        "country": "Yaponiya",
        "language": "O'zbek tilida",
        "year": 2002,
        "genre": "Sarguzasht, Ekshn",
        "link": "https://t.me/Haruki_animelaruzboty/2"
    },
    3: {
        "name": "Attack on Titan",
        "episodes": 75,
        "country": "Yaponiya",
        "language": "O'zbek tilida",
        "year": 2013,
        "genre": "Jangari, Dramatik",
        "link": "https://t.me/Haruki_animelaruzboty/3"
    },
    4: {
        "name": "One Piece",
        "episodes": 1100,
        "country": "Yaponiya",
        "language": "O'zbek tilida",
        "year": 1999,
        "genre": "Sarguzasht, Komediya",
        "link": "https://t.me/Haruki_animelaruzboty/4"
    },
    5: {
        "name": "Demon Slayer",
        "episodes": 55,
        "country": "Yaponiya",
        "language": "O'zbek tilida",
        "year": 2019,
        "genre": "Jangari, Fantastik",
        "link": "https://t.me/Haruki_animelaruzboty/5"
    }
}

# /start komandasi (tugmalar bilan)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Tugmalar
    keyboard = [
        [InlineKeyboardButton("📚 Anime ro'yxati", callback_data='list_anime')],
        [InlineKeyboardButton("🔍 Anime qidirish", callback_data='search_anime')],
        [InlineKeyboardButton("⭐ Top 5 Anime", callback_data='top_anime')],
        [InlineKeyboardButton("📞 Yordam", callback_data='help')],
        [InlineKeyboardButton("📢 Kanalimiz", url='https://t.me/Haruki_animelaruzboty')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f'👋 Assalomu alaykum {user.first_name}!\n\n'
        '🎌 *Anime Bot* ga xush kelibsiz!\n'
        'Quyidagi tugmalardan foydalaning:',
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Tugma bosilganda
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'list_anime':
        # Anime ro'yxati tugmasi
        keyboard = []
        for anime_id, anime in ANIMES.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"{anime_id}. {anime['name'][:20]}...",
                    callback_data=f'anime_{anime_id}'
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="📚 *Anime ro'yxati:*\n\nQuyidagilardan birini tanlang:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data.startswith('anime_'):
        # Anime tanlangan
        anime_id = int(query.data.split('_')[1])
        anime = ANIMES[anime_id]
        
        keyboard = [
            [InlineKeyboardButton("🔗 Kanalga o'tish", url=anime['link'])],
            [InlineKeyboardButton("📚 Boshqa anime", callback_data='list_anime')],
            [InlineKeyboardButton("🔙 Bosh menyu", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        info_text = f"""
🎬 *{anime['name']}*

📊 *Ma'lumotlar:*
🎥 Qismlar: {anime['episodes']} ta
🌐 Davlat: {anime['country']}
🇺🇿 Til: {anime['language']}
📅 Yil: {anime['year']}
🎞 Janr: {anime['genre']}

🔗 Tomosha qilish uchun pastdagi tugmani bosing!
        """
        
        await query.edit_message_text(
            text=info_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data == 'search_anime':
        # Qidiruv tugmasi
        await query.edit_message_text(
            text="🔍 *Anime qidirish*\n\n"
                 "Anime nomini yuboring:\n"
                 "Masalan: Naruto, Attack on Titan\n\n"
                 "Yoki raqam yuboring: 1, 2, 3...",
            parse_mode='Markdown'
        )
    
    elif query.data == 'top_anime':
        # Top anime tugmasi
        top_text = "⭐ *Top 5 Anime:*\n\n"
        
        for anime_id in [1, 2, 3, 4, 5]:
            if anime_id in ANIMES:
                anime = ANIMES[anime_id]
                top_text += f"{anime_id}. *{anime['name']}*\n"
                top_text += f"   ⭐ {anime['genre']}\n"
                top_text += f"   📅 {anime['year']}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("📚 Barcha anime", callback_data='list_anime')],
            [InlineKeyboardButton("🔙 Bosh menyu", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=top_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data == 'help':
        # Yordam tugmasi
        help_text = """
📞 *Bot yordami:*

1️⃣ *Anime ko'rish:* Ro'yxatdan tanlang yoki raqam yuboring
2️⃣ *Anime qidirish:* Nomini yozing yoki 🔍 tugmasini bosing
3️⃣ *Top anime:* Eng yaxshi anime lar ro'yxati

📢 *Kanalimiz:* @Haruki_animelaruzboty
⭐ *Taklif va shikoyatlar:* @sizning_username


/start - Boshlash
/help - Yordam
/list - Ro'yxat
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Bosh menyu", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=help_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data == 'back_to_main':
        # Asosiy menyuga qaytish
        keyboard = [
            [InlineKeyboardButton("📚 Anime ro'yxati", callback_data='list_anime')],
            [InlineKeyboardButton("🔍 Anime qidirish", callback_data='search_anime')],
            [InlineKeyboardButton("⭐ Top 5 Anime", callback_data='top_anime')],
            [InlineKeyboardButton("📞 Yordam", callback_data='help')],
            [InlineKeyboardButton("📢 Kanalimiz", url='https://t.me/Haruki_animelaruzboty')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text='🎌 *Anime Bot* ga xush kelibsiz!\nQuyidagi tugmalardan foydalaning:',
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# /help komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📞 *Bot yordami:*

1. Anime ko'rish uchun uning raqamini yuboring
   Masalan: 1, 2, 3

2. Anime qidirish uchun nomini yozing
   Masalan: Naruto

3. Barcha anime lar ro'yxati: /list

📢 *Kanalimiz:* @Haruki_animelaruzboty
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

# /list komandasi
async def list_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_text = "📚 *Barcha Anime lar:*\n\n"
    
    for anime_id, anime in ANIMES.items():
        list_text += f"{anime_id}. *{anime['name']}* ({anime['year']})\n"
        list_text += f"   📺 {anime['episodes']} qism | ⭐ {anime['genre']}\n\n"
    
    await update.message.reply_text(list_text, parse_mode='Markdown')

# Matn xabarlarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    
    # Agar raqam bo'lsa
    if user_input.isdigit():
        anime_id = int(user_input)
        if anime_id in ANIMES:
            anime = ANIMES[anime_id]
            
            # Tugmalar bilan javob
            keyboard = [
                [InlineKeyboardButton("🔗 Kanalga o'tish", url=anime['link'])],
                [InlineKeyboardButton("📚 Boshqa anime", callback_data='list_anime')],
                [InlineKeyboardButton("🏠 Bosh menyu", callback_data='back_to_main')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            info_text = f"""
🎬 *{anime['name']}*

📊 *Ma'lumotlar:*
🎥 Qismlar: {anime['episodes']} ta
🌐 Davlat: {anime['country']}
🇺🇿 Til: {anime['language']}
📅 Yil: {anime['year']}
🎞 Janr: {anime['genre']}

🔗 Tomosha qilish uchun pastdagi tugmani bosing!
            """
            
            await update.message.reply_text(
                info_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Bunday raqamdagi anime topilmadi.")
    
    # Agar matn bo'lsa (qidiruv)
    else:
        found_animes = []
        for anime_id, anime in ANIMES.items():
            if user_input.lower() in anime['name'].lower():
                found_animes.append(f"{anime_id}. *{anime['name']}*")
        
        if found_animes:
            response = "🔍 *Topilgan anime lar:*\n\n" + "\n".join(found_animes)
            response += "\n\nℹ️ To'liq ma'lumot uchun raqamini yuboring"
        else:
            response = "❌ Hech narsa topilmadi. /list buyrug'i bilan ro'yxatni ko'ring."
        
        await update.message.reply_text(response, parse_mode='Markdown')

# Xatolik handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Xatolik yuz berdi:", exc_info=context.error)
    try:
        await update.message.reply_text("❌ Kechirasiz, xatolik yuz berdi. Iltimos keyinroq urinib ko'ring.")
    except:
        pass

# Asosiy funksiya
def main():
    # Bot ilovasini yaratish
    application = Application.builder().token(TOKEN).build()
    
    # Handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))  # Tugma handler
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_anime))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Xatolik handler
    application.add_error_handler(error_handler)
    
    # Botni ishga tushirish
    print("🤖 Anime Bot ishga tushdi...")
    print("🎌 Tugmalar bilan ishlaydi")
    print("📡 Polling modeda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
