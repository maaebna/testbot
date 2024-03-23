from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Самые дешевые билеты", callback_data="cb_low"),
        InlineKeyboardButton("Самые дорогие билеты", callback_data="cb_high"),
        InlineKeyboardButton("Цены на несколько дат", callback_data="cb_custom"),
        InlineKeyboardButton("Просмотреть историю запросов", callback_data="cb_history"),
        InlineKeyboardButton("Обратная связь", callback_data="cb_feedback")
    )
    return markup


def handle_button(button):
    if button == "Самые дешевые билеты":
        return "/low"
    elif button == "Самые дорогие билеты":
        return "/high"
    elif button == "Цены на несколько дат":
        return "/custom"
    elif button == "Просмотреть историю запросов":
        return "/history"
    elif button == "Обратная связь":
        return "/feedback"


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    from handlers.message_handlers import low_command, high_command, custom_command, feedback_command
    if call.data == "cb_low":
        low_command(call.message)
    elif call.data == "cb_high":
        high_command(call.message)
    elif call.data == "cb_custom":
        custom_command(call.message)
    elif call.data == "cb_history":
        bot.send_message(call.message.chat.id, "Нажмите на команду /history, чтобы просмотреть историю запросов.")
    elif call.data == "cb_feedback":
        feedback_command(call.message)