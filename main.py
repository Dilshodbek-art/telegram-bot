import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Replace this with your actual bot token
BOT_TOKEN = "7191481336:AAEyEAfMdzAydvQldhaZU-WHuZaBQMg9QYY"

# Basic /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to MyLinguaPall Bot!\nType /help to see what I can do.")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Features:\n- Daily Word\n- Pronunciation\n- Quiz\n- Language Level Test\n\nComing soon...")

# Fallback for unknown messages
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Sorry, I didn't understand that. Type /help.")

# Run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    app.run_polling()

if __name__ == "__main__":
    main()
