import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from sqlalchemy import create_engine
from ai_engine import smart_analysis, whale_scan, auto_trade_execute

# ----------------------
# إعداد السجلّات
# ----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------
# إعداد قاعدة البيانات
# ----------------------
engine = create_engine("mysql+pymysql://root:password@localhost/smartbot")

# ----------------------
# خيارات اللغات
# ----------------------
LANG_TEXTS = {
    "ar": {
        "start": "مرحبا بك في SmartBot! اختر الخدمة:",
        "choose": "اختر الخدمة:",
        "analysis": "تحليل ذكي 📊",
        "whales": "تتبع الحيتان 🐋",
        "auto": "تداول آلي 🤖",
        "lang": "اللغة 🌐",
        "send_symbol": "أرسل رمز العملة / الذهب / السهم:",
        "working": "جار التحليل…",
        "done": "تم ✔",
    },
    "en": {
        "start": "Welcome to SmartBot! Choose a service:",
        "choose": "Choose a service:",
        "analysis": "Smart Analysis 📊",
        "whales": "Whale Tracking 🐋",
        "auto": "Auto Trading 🤖",
        "lang": "Language 🌐",
        "send_symbol": "Send the symbol (Crypto / Gold / Stock):",
        "working": "Processing…",
        "done": "Done ✔",
    }
}

# ----------------------
# حفظ لغة المستخدم
# ----------------------
user_lang = {}

def get_lang(user_id):
    return user_lang.get(user_id, "ar")

# ----------------------
# زرار البداية
# ----------------------
async def start(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(LANG_TEXTS[get_lang(uid)]["analysis"], callback_data="analysis")],
        [InlineKeyboardButton(LANG_TEXTS[get_lang(uid)]["whales"], callback_data="whales")],
        [InlineKeyboardButton(LANG_TEXTS[get_lang(uid)]["auto"], callback_data="auto")],
        [InlineKeyboardButton(LANG_TEXTS[get_lang(uid)]["lang"], callback_data="lang")]
    ]
    
    await update.message.reply_text(
        LANG_TEXTS[get_lang(uid)]["start"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ----------------------
# اختيار اللغة
# ----------------------
async def choose_language(update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("العربية 🇸🇦", callback_data="lang_ar")],
        [InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")]
    ]
    await query.edit_message_text(
        "اختر لغتك / Choose your language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ----------------------
# تطبيق اللغة
# ----------------------
async def set_language(update, context):
    query = update.callback_query
    uid = query.from_user.id

    if query.data == "lang_ar":
        user_lang[uid] = "ar"
    else:
        user_lang[uid] = "en"

    await query.answer()
    await start(update, context)

# ----------------------
# اختيار خدمة
# ----------------------
async def menu_handler(update, context):
    query = update.callback_query
    uid = query.from_user.id
    lang = get_lang(uid)

    await query.answer()

    if query.data == "analysis":
        context.user_data["mode"] = "analysis"
        await query.edit_message_text(LANG_TEXTS[lang]["send_symbol"])

    elif query.data == "whales":
        result = whale_scan()
        await query.edit_message_text(result)

    elif query.data == "auto":
        result = auto_trade_execute()
        await query.edit_message_text(result)

    elif query.data == "lang":
        await choose_language(update, context)

# ----------------------
# استقبال الرسائل
# ----------------------
async def handle_message(update, context):
    uid = update.effective_user.id
    lang = get_lang(uid)
    text = update.message.text

    if context.user_data.get("mode") == "analysis":
        await update.message.reply_text(LANG_TEXTS[lang]["working"])
        result = smart_analysis(text)
        await update.message.reply_text(result)
        context.user_data["mode"] = None

# ----------------------
# تشغيل البوت
# ----------------------
def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^(analysis|whales|auto|lang)$"))
    app.add_handler(CallbackQueryHandler(set_language, pattern="^(lang_ar|lang_en)$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
