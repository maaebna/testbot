from config import bot
import handlers.message_handlers

if __name__ == "__main__":
    bot.polling(none_stop=True)