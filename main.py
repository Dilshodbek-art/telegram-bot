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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes

# Sample quiz questions
quiz_questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Paris", "London", "Rome"],
        "correct": 1
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["Python", "HTML", "C++", "Java"],
        "correct": 1
    }
]

user_quiz_data = {}

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_quiz_data[user_id] = {"score": 0, "current_q": 0}
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = user_quiz_data[user_id]
    q_num = data["current_q"]

    if q_num < len(quiz_questions):
        question = quiz_questions[q_num]
        buttons = [
            [InlineKeyboardButton(opt, callback_data=str(i))] 
            for i, opt in enumerate(question["options"])
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        if update.callback_query:
            await update.callback_query.message.reply_text(question["question"], reply_markup=reply_markup)
        else:
            await update.message.reply_text(question["question"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"Quiz finished! Your score: {data['score']}/{len(quiz_questions)}")
        del user_quiz_data[user_id]

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = user_quiz_data[user_id]
    q_num = data["current_q"]
    selected = int(query.data)
    correct = quiz_questions[q_num]["correct"]

    if selected == correct:
        data["score"] += 1

    data["current_q"] += 1
    await query.answer()
    await send_question(update, context)
    application.add_handler(CommandHandler("quiz", quiz))
application.add_handler(CallbackQueryHandler(quiz_answer))
BotCommand("quiz", "Take a short quiz"),
async def set_commands(application):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("leveltest", "Take a level test"),
        BotCommand("dailyword", "Get today’s word"),
        BotCommand("quiz", "Take a short quiz")
    ]
    await application.bot.set_my_commands(commands)
