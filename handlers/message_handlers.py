import sqlite3
from config import bot
from database.create_database import save_message_to_db
from functions.end_of_func import end_of_func
from functions.flight_prices import get_lowest_price, get_custom_prices, get_highest_price
from keyboards.keyboard_creator import gen_markup


@bot.message_handler(commands=['help'])
def message_handler(message):
    bot.send_message(message.chat.id, "Доступные команды:", reply_markup=gen_markup())


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    bot.send_message(message.chat.id,
                     f"Привет, {username}! Я бот для поиска информации о ценах на авиабилеты."
                     "\nИспользуй команду /help, чтобы получить список команд.")


@bot.message_handler(commands=['low'])
def low_command(message):
    bot.send_message(message.chat.id, "Введите город вылета, город прилета, дату вылета и дату прилета"
                                      "\n\nНапример: Москва Санкт-Петербург 2024-04-10 2024-04-20"
                                      "\nЕсли обратный билет не нужен, введите только дату вылета:")
    bot.register_next_step_handler(message, get_lowest_price)


@bot.message_handler(commands=['high'])
def high_command(message):
    bot.send_message(message.chat.id, "Введите город вылета, город прилета, дату вылета и дату прилета"
                                      "\n\nНапример: Москва Санкт-Петербург 2024-04-10 2024-04-20"
                                      "\nЕсли обратный билет не нужен, введите только дату вылета:")
    bot.register_next_step_handler(message, get_highest_price)


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = ("Доступные команды:\n/low - получить минимальную цену билета"
                 "\n/high - получить максимальную цену билета"
                 "\n/custom - получить информацию о ценах в определенный период"
                 "\n/history - просмотреть историю запросов"
                 "\n/feedback - обратная связь")
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['custom'])
def custom_command(message):
    bot.send_message(message.chat.id,
                     "Введите город вылета🛫, город прилета🛬 и желаемые даты вылета"
                     "\n\nНапример: Москва Санкт-Петербург 2024-04-10 2024-04-20")
    bot.register_next_step_handler(message, get_custom_prices)


@bot.message_handler(commands=['feedback'])
def feedback_command(message):
    bot.send_message(message.chat.id, "Для обратной связи напишите мне - @maaebna")


@bot.message_handler(commands=['history'])
def history_command(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT message_text FROM user_messages WHERE user_id = ?", (user_id,))
    history = cursor.fetchall()
    conn.close()
    if history:
        messages = [message[0] for message in history]
        bot.send_message(message.chat.id, f"История ваших запросов: {', '.join(messages)}")
    else:
        bot.send_message(message.chat.id, "У вас пока нет истории запросов.")
    end_of_func(message)