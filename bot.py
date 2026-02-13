from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Define Menu Keys
MENU_KEYBOARD = [
    ["Our Services", "Why Us"],
    ["Latest Offers", "Contact Us"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! \n\n"
        "Welcome to <b>YMM Financial Services</b> Bot. \n"
        "We help with Investment, Insurance, and Wealth Growth.\n\n"
        "How can I assist you today?",
        reply_markup=ReplyKeyboardMarkup(MENU_KEYBOARD, one_time_keyboard=False, resize_keyboard=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Tap on the menu buttons to explore our services.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle menu button clicks."""
    text = update.message.text

    if text == "Our Services":
        response = (
            "<b>Our Services:</b>\n"
            "📈 <b>Investment & Wealth Growth:</b> Strategic planning for long-term growth.\n"
            "🛡️ <b>Insurance Protection:</b> Comprehensive coverage for family.\n"
            "💰 <b>Loan Solutions:</b> Competitive rates for all needs.\n"
            "⚖️ <b>Tax & Compliance:</b> Expert filing and advisory."
        )
    elif text == "Why Us":
        response = (
            "<b>Why Choose Us?</b>\n"
            "✅ Expert Advisors\n"
            "✅ Transparent Pricing\n"
            "✅ Quick Processing\n"
            "✅ Personalized Support"
        )
    elif text == "Latest Offers":
        response = (
            "<b>🔥 Latest Updates & Offers:</b>\n\n"
            "1️⃣ <b>Free Demat Account:</b> Open with Zerodha & get ₹200 brokerage credit!\n"
            "2️⃣ <b>Personal Loan:</b> Rates starting @ 10.5% – Apply now!\n"
            "3️⃣ <b>Webinar:</b> 'How to Build Wealth in 2025' – Register Now!"
        )
    elif text == "Contact Us":
        response = (
            "<b>📞 Get in Touch!</b>\n\n"
            "<b>Call/WhatsApp:</b> +91-8445744581\n"
            "<b>Email:</b> harsh1991mishra@gmail.com\n"
            "<b>Address:</b> Majestic Signia, A-27, Block –A, Industrial Area, Sector – 62, Noida."
        )
    else:
        response = "I didn't understand that command. Please use the menu buttons."

    await update.message.reply_html(response)

def main() -> None:
    """Start the bot."""
    # Token provided by user
    TOKEN = "8419054231:AAHQne4lvzzJMFQbEuLxosjKv6G5aspGYzA" 
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
