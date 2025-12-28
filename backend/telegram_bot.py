import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from ai_core import chat_answer

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or "PUT_YOUR_TOKEN_HERE"


# =========================
# DASHBOARD KEYBOARD
# =========================
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Market Analysis", callback_data="analysis")],
        [InlineKeyboardButton("🐋 Whale Alerts", callback_data="whales")],
        [InlineKeyboardButton("🕌 Halal Screening", callback_data="halal")],
        [InlineKeyboardButton("🤖 Auto Trading", callback_data="autotrade")],
        [InlineKeyboardButton("📂 My History", callback_data="history")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]
    return InlineKeyboardMarkup(keyboard)


# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *SmartBot Dashboard*\n\n"
        "Analyze crypto, gold & halal stocks.\n"
        "Paper first. Live later.\n\n"
        "اختر من اللوحة 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )


# =========================
# BUTTON HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "analysis":
        await query.edit_message_text(
            "📊 *Market Analysis*\n\n"
            "اكتب مثال:\n"
            "- Analyze BTC\n"
            "- تحليل الذهب\n"
            "- AAPL analysis",
            parse_mode="Markdown"
        )

    elif data == "whales":
        answer = chat_answer("Whale alerts today", guest=True)
        await query.edit_message_text(f"🐋 *Whale Alerts*\n\n{answer}", parse_mode="Markdown")

    elif data == "halal":
        await query.edit_message_text(
            "🕌 *Halal Screening*\n\n"
            "اكتب:\n"
            "- Is AAPL halal?\n"
            "- MSFT halal?",
            parse_mode="Markdown"
        )

    elif data == "autotrade":
        await query.edit_message_text(
            "🤖 *Auto Trading*\n\n"
            "Mode: Paper\n"
            "Status: 🟢 Ready\n\n"
            "Live trading 🔒 (soon)",
            parse_mode="Markdown"
        )

    elif data == "history":
        await query.edit_message_text(
            "📂 *History*\n\n"
            "آخر التحاليل ستظهر هنا قريبًا.",
            parse_mode="Markdown"
        )

    elif data == "settings":
        await query.edit_message_text(
            "⚙️ *Settings*\n\n"
            "Language: AR / EN\n"
            "Notifications: ON",
            parse_mode="Markdown"
        )


# =========================
# MESSAGE HANDLER (AI)
# =========================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    answer = chat_answer(
        question=text,
        user_id=str(update.message.from_user.id),
        guest=True
    )

    await update.message.reply_text(answer)


# =========================
# RUN BOT
# =========================
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("🤖 Telegram Bot running...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()
