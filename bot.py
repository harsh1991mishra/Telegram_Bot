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
    ["Latest Offers", "Contact Us"],
    ["My Portfolio", "Certifications"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! \n\n"
        "Welcome to <b>Harsh Mishra's (@Baba1991bot)</b> Assistant. \n"
        "I can help you with Financial Services (YMM) or show you Harsh's Portfolio.\n\n"
        "<i>'I am the one who knocks!' - Breaking Bad</i>\n\n"
        "Select an option below:",
        reply_markup=ReplyKeyboardMarkup(MENU_KEYBOARD, one_time_keyboard=False, resize_keyboard=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Tap on the menu buttons to explore.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle menu button clicks."""
    text = update.message.text

    if text == "Our Services":
        response = (
            "<b>Our Services:</b>\n"
            "📈 <b>Investment & Wealth Growth:</b> Strategic planning.\n"
            "🛡️ <b>Insurance Protection:</b> Coverage for family.\n"
            "💰 <b>Loan Solutions:</b> Competitive rates.\n"
            "⚖️ <b>Tax & Compliance:</b> Expert filing."
        )
    elif text == "Why Us":
        response = (
            "<b>Why Choose Us?</b>\n"
            "✅ Expert Advisors (Senior Recruiter @ AltezzaSys)\n"
            "✅ Transparent Pricing\n"
            "✅ Quick Processing\n"
            "✅ Personalized Support"
        )
    elif text == "Latest Offers":
        response = (
            "<b>🔥 Latest Updates & Offers:</b>\n\n"
            "1️⃣ <b>Free Demat Account:</b> Open with Zerodha & get ₹200 credit.\n"
            "2️⃣ <b>Personal Loan:</b> Rates starting @ 10.5%.\n"
            "3️⃣ <b>Portfolio Launch:</b> Check out <a href='https://harsh1991mishra.github.io'>harsh1991mishra.github.io</a>"
        )
    elif text == "Contact Us":
        response = (
            "<b>📞 Get in Touch!</b>\n\n"
            "<b>Name:</b> Harsh Mishra\n"
            "<b>Call/WhatsApp:</b> +91-8445744581\n"
            "<b>Email:</b> harsh1991mishra@gmail.com\n"
            "<b>Office:</b> Majestic Signia, A-27, Sec-62, Noida.\n"
            "<b>Web:</b> <a href='https://about.me/harsh1991mishra'>About Me</a>"
        )
    elif text == "My Portfolio":
        response = (
            "<b>🚀 Harsh Mishra's Portfolio</b>\n\n"
            "<i>Data Analyst & AI Frontier | Cyber Security Enthusiast</i>\n\n"
            "🔗 <b>Website:</b> <a href='https://harsh1991mishra.github.io'>harsh1991mishra.github.io</a>\n"
            "🔗 <b>Data Science:</b> <a href='http://www.datascienceportfol.io/harsh1991mishra'>datascienceportfol.io</a>\n"
            "🔗 <b>Salesforce:</b> <a href='https://www.salesforce.com/trailblazer/harsh1991mishra'>Trailblazer Profile</a>\n"
            "🔗 <b>Hackster:</b> <a href='https://www.hackster.io/'>Hackster.io</a>\n\n"
            "#DataAnalytics #AI #CyberSecurity"
        )
    elif text == "Certifications":
        response = (
            "<b>🏆 7 Days = 7 Certificates Challenge</b>\n\n"
            "1️⃣ <b>Google:</b> Developers Certification\n"
            "2️⃣ <b>PayPal:</b> Technical Compliance / PCI\n"
            "3️⃣ <b>Deloitte:</b> Academy Learning\n"
            "4️⃣ <b>Oracle:</b> Java/SQL Certifications\n"
            "5️⃣ <b>IBM:</b> Professional Certs\n"
            "6️⃣ <b>Meta:</b> Business Certification\n"
            "7️⃣ <b>Microsoft:</b> Python Development"
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
