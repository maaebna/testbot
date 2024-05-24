# README

Этот код представляет собой Telegram-бот для поиска информации о ценах на авиабилеты.
Бот использует библиотеки Telebot и requests для интеграции с Telegram и выполнения HTTP-запросов соответственно.
Также используется библиотека sqlite3 для управления локальной базой данных, в которой хранятся сообщения пользователей.

## Особенности

Бот предоставляет следующие команды:

- `/low` - получить самую низкую цену на авиабилет
- Пример запроса: https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin=MOW&destination=UFA&departure_at=2024-04-01&return_at=&unique=false&sorting=price&direct=false&cy=usd&limit=30&page=1&one_way=false&token=3103bb870e29d162bbde639cc4ce40ba
- Что используется в ответе API: "departure_at":"2024-04-01T12:10:00+03:00","destination":"UFA","return_at":"2024-04-03T17:00:00+05:00","origin":"MOW","price":10449
- `/high` - получить самую высокую цену на авиабилет
- Пример запроса: https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin=MOW&destination=UFA&departure_at=2024-04-01&return_at=2024-04-10&unique=false&sorting=price&direct=false&cy=usd&limit=30&page=1&one_way=false&token=3103bb870e29d162bbde639cc4ce40ba
- Что используется в ответе API: "departure_at":"2024-04-01T11:40:00+03:00","destination":"UFA","return_at":"2024-04-18T16:55:00+05:00","origin":"MOW","price":16587
- `/custom` - получить информацию о ценах на авиабилеты в определенные даты
- Пример запроса: https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin=MOW&destination=UFA&departure_at=2024-04-01&return_at=&unique=false&sorting=price&direct=false&cy=usd&limit=30&page=1&one_way=false&token=3103bb870e29d162bbde639cc4ce40ba
- Что используется в ответе API: "departure_at":"2024-04-02T09:20:00+03:00","destination":"UFA","return_at":"2024-04-03T06:55:00+05:00","origin":"MOW","price":8142
- `/history` - просмотр истории запросов пользователей
- `/feedback` - отправить обратную связь

## База данных

Бот использует базу данных SQLite с названием `bot_database.db` для хранения сообщений пользователей.
Он создает таблицу `user_messages` с колонками `id`, `user_id`, `message_text` и `message_date` для хранения сообщений пользователей.

## Интеграция с API

Бот интегрируется с API TravelPayouts для получения информации о ценах на авиабилеты для разных дат и мест.
Для выполнения HTTP-запросов к API и обработки JSON-ответов используется библиотека `requests`.

## Реализация

Бот реализован с использованием библиотеки `telebot` для обработки функциональности бота Telegram.
Он определяет обработчики сообщений для различных команд и обратных вызовов кнопок для взаимодействия с пользователями.
Бот также обрабатывает ввод пользователя, разбирает даты и предоставляет соответствующие ответы на основе запросов пользователя.

## Начало работы

Для запуска бота вам необходимо в терминале запустить команду `python3 main.py`
Убедитесь, что установлены необходимые библиотеки с помощью `pip3 install pyTelegramBotAPI requests`

## Использование

Перед запуском бота убедитесь, что файл `bot_database.db` доступен для хранения сообщений пользователей.
После запуска бота пользователи могут взаимодействовать с ним, отправляя команды в чат Telegram.
Бот будет отвечать информацией о ценах на авиабилеты на основе запросов пользователя.

## Поддержка

По любым вопросам или обратной связи вы можете обратиться к создателю бота.
Используйте команду `/feedback` или свяжитесь напрямую в Telegram - @maaebna.


```bash
pip3 install pyTelegramBotAPI requests
python3 main.py
