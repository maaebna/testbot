import requests
import locale
from datetime import datetime
from config import bot
from database.create_database import save_message_to_db
from functions.end_of_func import end_of_func
from keyboards.keyboard_creator import gen_markup

API_KEY = "3103bb870e29d162bbde639cc4ce40ba"


def get_iata_codes(search_query):
    url = "https://api.travelpayouts.com/data/ru/cities.json?_gl=1*l6ylpl*_ga*MTcxMzY4NDg3Mi4xNzA5ODE4OTgz*_ga_1WLL0NEBEH*MTcwOTkzMzU3Ny40LjEuMTcwOTkzMzcxOS42MC4wLjA."
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for city in data:
            if city['name'] is not None and search_query in city['name']:
                return city['code']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def get_lowest_price(message):
    bot.send_message(message.chat.id, "Ищу билет...")
    try:
        departure_city, arrival_city, depart_date, *return_date = message.text.split()
        if len(return_date) > 0:
            return_date = return_date[0]
        else:
            return_date = ""
        origin = get_iata_codes(departure_city)
        destination = get_iata_codes(arrival_city)
        if origin is not None and destination is not None:
            save_message_to_db(message.from_user.id, message.text)
            if return_date:
                url = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={origin}&destination={destination}&departure_at={depart_date}&return_at={return_date}&unique=false&sorting=price&direct=false&cy=usd&limit=30&page=1&one_way=false&token={API_KEY}"
            else:
                url = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={origin}&destination={destination}&departure_at={depart_date}&return_at={return_date}&&unique=false&sorting=price&direct=false&cy=usd&limit=30&page=1&one_way=true&token={API_KEY}"
            response = requests.get(url)
            data = response.json()
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
            departure_datetime = datetime.strptime(data['data'][0]['departure_at'], "%Y-%m-%dT%H:%M:%S%z")
            formatted_departure_datetime = departure_datetime.strftime("%A, %d %B %Y %H:%M")
            lowest_price = data['data'][0]['price']
            lowest_price_link = data['data'][0]['link']
            bot.send_message(message.chat.id, f"Минимальная цена билета - {lowest_price} руб. "
                                              f"\n\nДата и время вылета - {formatted_departure_datetime}"
                                              f"\n\nСсылка на покупку: aviasales.ru{lowest_price_link}")
        else:
            bot.send_message(message.chat.id, "Не удалось найти коды для указанных городов.")
        end_of_func(message)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите город вылета, город прилета и даты в правильном формате.")
    except Exception as e:
        bot.send_message(message.chat.id, "Что-то пошло не так."
                                          "\n\nПожалуйста, вызовите команду /low еще раз и проверьте корректность ваших данных.")


def get_highest_price(message):
    bot.send_message(message.chat.id, "Ищу билет...")
    try:
        departure_city, arrival_city, depart_date, *return_date = message.text.split()
        if len(return_date) > 0:
            return_date = return_date[0]
        else:
            return_date = ""
        origin = get_iata_codes(departure_city)
        destination = get_iata_codes(arrival_city)
        if origin is not None and destination is not None:
            save_message_to_db(message.from_user.id, message.text)
            if return_date:
                url = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={origin}&destination={destination}&departure_at={depart_date}&return_at={return_date}&unique=false&sorting=price&direct=false&cy=usd&limit=30&page=1&one_way=false&token={API_KEY}"
            else:
                url = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={origin}&destination={destination}&departure_at={depart_date}&return_at={return_date}&unique=false&sorting=price&direct=false&cy=usd&limit=30&page=1&one_way=true&token={API_KEY}"
            response = requests.get(url)
            data = response.json()

            if data['data']:
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                departure_datetime = datetime.strptime(data['data'][0]['departure_at'], "%Y-%m-%dT%H:%M:%S%z")
                formatted_departure_datetime = departure_datetime.strftime("%A, %d %B %Y %H:%M")
                max_price_ticket = max(data['data'], key=lambda x: x['price'])
                highest_price = max_price_ticket['price']
                highest_price_link = max_price_ticket['link']
                bot.send_message(message.chat.id, f"Максимальная цена билета - {highest_price} руб."
                                                  f"\n\nДата и время вылета - {formatted_departure_datetime}"
                                                  f"\n\nСсылка на покупку: aviasales.ru{highest_price_link}")
            else:
                bot.send_message(message.chat.id, "Для указанных городов и дат билеты не найдены.")
        else:
            bot.send_message(message.chat.id, "Не удалось найти коды для указанных городов.")
        end_of_func(message)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите город вылета, город прилета и дату в правильном формате.")
    except Exception as e:
        bot.send_message(message.chat.id, "Что-то пошло не так."
                                          "\n\nПожалуйста, вызовите команду /high еще раз и проверьте корректность ваших данных.")


def get_custom_prices(message):
    save_message_to_db(message.from_user.id, message.text)
    bot.send_message(message.chat.id, "Ищу билеты...")
    departure_city, arrival_city, *departure_dates = message.text.split()
    prices = []
    origin = get_iata_codes(departure_city)
    destination = get_iata_codes(arrival_city)
    for date in departure_dates:
        url = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={origin}&destination={destination}&departure_at={date}&unique=false&sorting=price&direct=false&cy=rub&limit=30&page=1&one_way=true&token={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data.get('data'):
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
            departure_datetime = datetime.strptime(data['data'][0]['departure_at'], "%Y-%m-%dT%H:%M:%S%z")
            formatted_departure_datetime = departure_datetime.strftime("%d %B %Y %H:%M")
            lowest_price = data['data'][0]['price']
            prices.append((date, lowest_price))
            bot.send_message(message.chat.id, f"Самый дешевый билет на {formatted_departure_datetime} обойдется вам в {lowest_price} руб."
                                              f"\n\nСсылка на покупку: aviasales.ru{data['data'][0]['link']}")
        else:
            bot.send_message(message.chat.id, f"Для {date} нет данных о ценах"
                                              f"\n\nПожалуйста, вызовите команду /custom еще раз и проверьте корректность ваших данных.")
            prices.append((date, "N/A"))
    end_of_func(message)
    return prices