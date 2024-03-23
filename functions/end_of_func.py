from config import bot
from keyboards.keyboard_creator import gen_markup


def end_of_func(message):
    bot.send_message(message.chat.id, "☁️✈" * 8)
    bot.send_message(message.chat.id, "Доступные команды:", reply_markup=gen_markup())