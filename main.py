import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Put your bot token here
BOT_TOKEN = "7191481336:AAEyEAfMdzAydvQldhaZU-WHuZaBQMg9QYY"

# States for conversation
QUESTION = 1

# Daily words example list (expand as needed)
daily_words = [
    ("serendipity", "the occurrence of events by chance in a happy way"),
    ("ephemeral", "lasting for a very short time"),
    ("loquacious", "very talkative"),
]

# Quiz questions (10)
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
        "👋 Hello! Welcome to MyLinguaPal bot.\n"
        "Commands:\n"
        "/dailyword - get daily word\n"
        "/test - start level test\n"
        "/cancel - stop the test"
    )

async def dailyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    word, meaning = daily_words[day_of_year % len(daily_words)]
    await update.message.reply_text(f"📚 Daily Word:\n*{word}*\nMeaning: {meaning}", parse_mode='Markdown')

async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['current_q'] = 0
    context.user_data['mistakes'] = []
    await update.message.reply_text(f"Starting level test! Question 1:\n{questions[0]['q']}")
    return QUESTION

async def test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text.strip().lower()
    current_q = context.user_data['current_q']
    correct_answer = questions[current_q]['a'].lower()

    if user_answer != correct_answer:
        context.user_data['mistakes'].append({
            "question": questions[current_q]['q'],
            "your_answer": update.message.text,
            "correct_answer": questions[current_q]['a']
        })

    current_q += 1
    if current_q < len(questions):
        context.user_data['current_q'] = current_q
        await update.message.reply_text(f"Question {current_q + 1}:\n{questions[current_q]['q']}")
        return QUESTION
    else:
        # Test ended
        mistakes = context.user_data['mistakes']
        if mistakes:
            reply = "Test completed! Here are the questions you missed:\n"
            for m in mistakes:
                reply += f"\n❌ Q: {m['question']}\nYour answer: {m['your_answer']}\nCorrect answer: {m['correct_answer']}\n"
        else:
            reply = "🎉 Congratulations! You answered all questions correctly."

        await update.message.reply_text(reply)
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Test cancelled. You can start again anytime with /test.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('test', test_start)],
        states={
            QUESTION: [MessageHandler(filters.TEXT & (~filters.COMMAND), test_answer)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('dailyword', dailyword))
    app.add_handler(conv_handler)

    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()
    from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Define the main menu keyboard
menu_keyboard = [['Level Test', 'Daily Word'], ['Help', 'About']]
menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Choose an option below:",
        reply_markup=menu_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Level Test":
        await update.message.reply_text("Starting your level test...")
        # Call your level test function here
        # e.g. await start_level_test(update, context)
    elif text == "Daily Word":
        await update.message.reply_text("Here's your daily word...")
        # Call your daily word function here
    elif text == "Help":
        await update.message.reply_text("Help info here.")
    elif text == "About":
        await update.message.reply_text("About info here.")
    else:
        await update.message.reply_text("Please choose an option from the menu.")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7191481336:AAEyEAfMdzAydvQldhaZU-WHuZaBQMg9QYY").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
