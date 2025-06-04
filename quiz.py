from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

quiz_questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "correct": 2
    },
    {
        "question": "What does 'Hola' mean in Spanish?",
        "options": ["Bye", "Hello", "Please", "Thanks"],
        "correct": 1
    }
]

user_quiz_progress = {}

def start_quiz(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_quiz_progress[user_id] = 0
    send_question(update, context, user_id)

def send_question(update: Update, context: CallbackContext, user_id):
    index = user_quiz_progress[user_id]
    if index < len(quiz_questions):
        q = quiz_questions[index]
        buttons = [
            [InlineKeyboardButton(opt, callback_data=str(i))]
            for i, opt in enumerate(q["options"])
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        context.bot.send_message(
            chat_id=user_id,
            text=q["question"],
            reply_markup=reply_markup
        )
    else:
        context.bot.send_message(chat_id=user_id, text="🎉 Quiz completed!")

def handle_answer(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    index = user_quiz_progress.get(user_id, 0)
    if index >= len(quiz_questions):
        return

    selected = int(query.data)
    correct = quiz_questions[index]["correct"]

    if selected == correct:
        query.edit_message_text("✅ Correct!")
    else:
        query.edit_message_text(
            f"❌ Wrong! The correct answer was: {quiz_questions[index]['options'][correct]}"
        )

    user_quiz_progress[user_id] += 1
    send_question(update, context, user_id)

def get_quiz_handler():
    return [
        CommandHandler("quiz", start_quiz),
        CallbackQueryHandler(handle_answer)
    ]
