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
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import asyncio
import datetime

# A sample list of daily words — you can expand this later
daily_words = [
    {"word": "hello", "definition": "A greeting", "translation": "salom"},
    {"word": "book", "definition": "A set of written pages", "translation": "kitob"},
    {"word": "sun", "definition": "The star at the center of our solar system", "translation": "quyosh"},
    # Add more words here...
]

# Store users who asked to receive daily words
subscribed_users = set()

async def send_daily_word(app):
    while True:
        now = datetime.datetime.now()
        if now.hour == 9:  # Send daily word at 09:00 AM server time
            for user_id in subscribed_users:
                word = daily_words[now.day % len(daily_words)]
                text = f"📘 Daily Word:\n\n🔤 *{word['word'].capitalize()}*\n📝 {word['definition']}\n🌍 Translation: {word['translation']}"
                await app.bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")
            await asyncio.sleep(3600)  # wait 1 hour before next check
        else:
            await asyncio.sleep(60)  # check every minute

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Welcome to MyLinguaPal bot.\nType /daily to get a daily word!")

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    subscribed_users.add(user_id)
    await update.message.reply_text("✅ You're now subscribed to daily words!")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7191481336:AAEyEAfMdzAydvQldhaZU-WHuZaBQMg9QYY").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("daily", daily))

    # Start background task for sending daily words
    app.job_queue.run_once(lambda ctx: asyncio.create_task(send_daily_word(app)), when=0)

    app.run_polling()
