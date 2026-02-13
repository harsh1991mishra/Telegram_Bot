import logging
import subprocess
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = "8419054231:AAHQne4lvzzJMFQbEuLxosjKv6G5aspGYzA"
ADMIN_PASSWORD = "Baba@8982"  # Password to become authorized
AUTHORIZED_USERS = set()      # Stores user_ids of authorized users

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Menus ---
MAIN_MENU = [["🕵️ OSINT Tools", "📡 WiFi Hacking"], ["ℹ️ Help", "🛑 Logout"]]

OSINT_MENU = [
    ["Recon-ng", "Maltego", "theHarvester"],
    ["Shodan", "Google Dorks", "SpiderFoot"],
    ["Arikon", "Sherlock", "Photon"],
    ["Creepy", "🔙 Back"]
]

WIFI_MENU = [
    ["Aircrack-ng", "Wireshark", "Reaver"],
    ["Wifite", "Kismet", "Fluxion"],
    ["Fern WiFi", "PixieWPS", "Bulbasaur"],
    ["WiFi Pumpkin", "🔙 Back"]
]

# --- Auth Decorator ---
def authorized_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user.id not in AUTHORIZED_USERS:
            await update.message.reply_text(
                "⛔ <b>Access Denied</b>\n"
                "You are not authorized to use these tools.\n"
                "Please run <code>/login THIS_BOTS_PASSWORD</code> to authenticate.",
                parse_mode="HTML"
            )
            return
        return await func(update, context)
    return wrapper

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    user = update.effective_user
    await update.message.reply_html(
        f"💀 <b>Mahakaal OS Bot</b> 💀\n\n"
        f"Greetings, {user.mention_html()}.\n"
        "I am your interface for OSINT and Network Operations.\n\n"
        "⚠️ <b>WARNING</b>: Authorized use only. All actions are logged.",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True),
    )

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Authenticate the user."""
    user = update.effective_user
    if not context.args:
        await update.message.reply_text("Usage: /login <password>")
        return

    password = context.args[0]
    if password == ADMIN_PASSWORD:
        AUTHORIZED_USERS.add(user.id)
        await update.message.reply_text(
            "✅ <b>Authentication Successful</b>\n"
            "You now have access to the arsenal.",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        )
        logger.info(f"User {user.id} ({user.username}) logged in.")
    else:
        await update.message.reply_text("❌ <b>Invalid Password</b>", parse_mode="HTML")
        logger.warning(f"Failed login attempt by {user.id} ({user.username}).")

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the user out."""
    user = update.effective_user
    if user.id in AUTHORIZED_USERS:
        AUTHORIZED_USERS.remove(user.id)
        await update.message.reply_text("🔒 <b>Logged Out</b>", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    else:
        await update.message.reply_text("You are not logged in.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help text."""
    await update.message.reply_html(
        "<b>Mahakaal Bot Help</b>\n\n"
        "<b>Navigation:</b> Use the menu buttons.\n"
        "<b>Tools:</b> Select a tool to see its usage or execute a command.\n"
        "<b>Safety:</b> Some tools require root privileges or GUI access.\n"
        "<b>Auth:</b> Use /login and /logout to manage access."
    )

# --- Tool Execution Logic ---

def execute_command(command):
    """Executes a shell command and returns output."""
    try:
        # Safety: Using shell=True is risky if input is untrusted. 
        # In a real scenario, use list args. Here we assume authorized user input.
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30 # 30s timeout
        )
        output = result.stdout if result.stdout else result.stderr
        if not output: 
            return "✅ Command executed (No Output)"
        return f"<code>{output[:4000]}</code>" # Telegram limit
    except subprocess.TimeoutExpired:
        return "❌ Command timed out."
    except Exception as e:
        return f"❌ Error: {str(e)}"

@authorized_only
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    
    # Navigation
    if text == "🕵️ OSINT Tools":
        await update.message.reply_text("Select an OSINT Target:", reply_markup=ReplyKeyboardMarkup(OSINT_MENU, resize_keyboard=True))
        return
    elif text == "📡 WiFi Hacking":
        await update.message.reply_text("Select a WiFi Module:", reply_markup=ReplyKeyboardMarkup(WIFI_MENU, resize_keyboard=True))
        return
    elif text == "🔙 Back":
        await update.message.reply_text("Main Menu:", reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))
        return
    elif text == "🛑 Logout":
        await logout(update, context)
        return

    # OSINT Tools
    if text == "Recon-ng":
        response = "<b>Recon-ng</b> is an interactive framework.\n\nRun in terminal:\n<code>sudo recon-ng</code>"
    elif text == "Maltego":
        response = "<b>Maltego</b> is a GUI application.\n\nRun in terminal:\n<code>maltego</code>"
    elif text == "theHarvester":
        response = "<b>theHarvester</b>: Email gathering.\n\nUsage: `/exec theHarvester -d target.com -b google`"
    elif text == "Shodan":
        response = "<b>Shodan</b>: Search Engine for IoT.\n\nUsage: `/exec shodan search <query>`\n(Requires API key init)"
    elif text == "Google Dorks":
        response = "<b>Google Dorks</b>: Advanced Search.\n\nTry searching for:\n`site:target.com filetype:pdf`"
    elif text == "SpiderFoot":
        response = "<b>SpiderFoot</b>: Automator.\n\nRun server:\n<code>spiderfoot -l 127.0.0.1:5001</code>"
    elif text == "Arikon":
        response = "<b>Arikon</b>: Automated OSINT.\n\nCheck repo for usage."
    elif text == "Sherlock":
        response = "<b>Sherlock</b>: Username search.\n\nUsage: `/exec sherlock <username>`"
    elif text == "Photon":
        response = "<b>Photon</b>: Website Crawler.\n\nUsage: `/exec python3 photon.py -u http://target.com`"
    elif text == "Creepy":
        response = "<b>Creepy</b>: Geolocation.\n\nRun GUI:\n<code>creepy</code>"

    # WiFi Tools
    elif text == "Aircrack-ng":
        response = "<b>Aircrack-ng</b>: Packet Analysis.\n\nCheck monitor mode:\n`/exec sudo airmon-ng`"
    elif text == "Wireshark":
        response = "<b>Wireshark</b>: Network Protocol Analyzer.\n\nRun GUI:\n<code>sudo wireshark</code>"
    elif text == "Reaver":
        response = "<b>Reaver</b>: WPS Attack.\n\nUsage:\n<code>sudo reaver -i wlan0mon -b <BSSID> -vv</code>"
    elif text == "Wifite":
        response = "<b>Wifite</b>: Automated Wireless Auditor.\n\nRun interactive:\n<code>sudo wifite</code>"
    elif text == "Kismet":
        response = "<b>Kismet</b>: Wireless Sniffer.\n\nRun server:\n<code>sudo kismet</code>"
    elif text == "Fluxion":
        response = "<b>Fluxion</b>: Evil Twin Attack.\n\nRun interactive:\n<code>sudo ./fluxion.sh</code>"
    elif text == "Fern WiFi":
        response = "<b>Fern WiFi Cracker</b>: GUI specific.\n\nRun:\n<code>sudo fern-wifi-cracker</code>"
    elif text == "PixieWPS":
        response = "<b>PixieWPS</b>: WPS Offline Dust.\n\nUsed with Reaver."
    elif text == "Bulbasaur":
        response = "<b>Bulbasaur</b>: Network Recon.\n\nCheck installation."
    elif text == "WiFi Pumpkin":
        response = "<b>WiFi Pumpkin 3</b>: Rogue AP.\n\nRun:\n<code>sudo wifipumpkin3</code>"
    
    else:
        response = "Unknown command or menu item."

    await update.message.reply_html(response)

@authorized_only
async def exec_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /exec command to run arbitrary shell commands."""
    cmd = ' '.join(context.args)
    if not cmd:
        await update.message.reply_text("Usage: /exec <command>")
        return
    
    await update.message.reply_text(f"⏳ Executing: `{cmd}`...", parse_mode="Markdown")
    
    # Security: In a real environment, strictly filter `cmd` here.
    output = execute_command(cmd)
    await update.message.reply_html(output)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("logout", logout))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("exec", exec_command))
    
    # Generic message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    print("Bot is polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
