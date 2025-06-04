from quiz import get_quiz_handler
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import datetime
import asyncio

# Replace with your actual bot token
BOT_TOKEN = "7191481336:AAEyEAfMdzAydvQldhaZU-WHuZaBQMg9QYY"

# Conversation states
QUESTION = 1

# Sample daily words (you can expand)
daily_words = [
    ("serendipity", "the occurrence of events by chance in a happy way"),
    ("ephemeral", "lasting for a very short time"),
    ("loquacious", "very talkative"),
]

# Level test questions (10 questions)
questions = [
    {"q": "What is the capital of France?", "a": "Paris"},
    {"q": "2 + 2 = ?", "a": "4"},
    {"q": "What color is the sky on a clear day?", "a": "Blue"},
    {"q": "How many legs does a spider have?", "a": "8"},
    {"q": "What is the opposite of hot?", "a": "Cold"},
    {"q": "What planet do we live on?", "a": "Earth"},
    {"q": "What is the past tense of 'go'?", "a": "Went"},
    {"q": "How many days are in a week?", "a": "7"},
    {"q": "What is the first letter of the alphabet?", "a": "A"},
    {"q": "What do bees produce?", "a": "Honey"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Welcome to MyLinguaPal bot.\n"
        "Use /dailyword to get today's word.\n"
        "Use /test to start the level test.\n"
        "Use /cancel to stop the test anytime."
    )
    await application.bot.set_my_commands([
    BotCommand("start", "Start the bot"),
    BotCommand("dailyword", "Get daily word"),
    BotCommand("test", "Start level test"),
    BotCommand("quiz", "Start a short quiz"),
    BotCommand("cancel", "Cancel current action")
])

async def dailyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pick daily word based on day of year (cycles through daily_words)
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    word, meaning = daily_words[day_of_year % len(daily_words)]
    await update.message.reply_text(f"📚 Daily Word:\n{word}\nMeaning: {meaning}")

async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['current_q'] = 0
    context.user_data['mistakes'] = []
    await update.message.reply_text(f"Starting level test. Question 1:\n{questions[0]['q']}")
    return QUESTION

async def test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text.strip()
    current_q = context.user_data['current_q']
    correct_answer = questions[current_q]['a']

    if user_answer.lower() != correct_answer.lower():
        context.user_data['mistakes'].append((questions[current_q]['q'], correct_answer))

    current_q += 1
    if current_q >= len(questions):
        # Test finished
        if context.user_data['mistakes']:
            text = "You made mistakes on these questions:\n\n"
            for q, a in context.user_data['mistakes']:
                text += f"Q: {q}\nCorrect answer: {a}\n\n"
        else:
            text = "🎉 Congratulations! You answered all questions correctly."

        await update.message.reply_text(text)
        return ConversationHandler.END
    else:
        context.user_data['current_q'] = current_q
        await update.message.reply_text(f"Question {current_q + 1}:\n{questions[current_q]['q']}")
        return QUESTION

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Test cancelled. Use /test to start again.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("test", test_start)],
        states={
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, test_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dailyword", dailyword))
    app.add_handler(conv_handler)

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
    application.add_handler(CommandHandler("quiz", quiz_start))
    from quiz import quiz_start

def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # other handlers...
    application.add_handler(CommandHandler("quiz", quiz_start))

    application.run_polling()
