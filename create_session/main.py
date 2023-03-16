from telethon import TelegramClient, events

# конфигурационные настройки
api_id = ""
api_hash = ''
phone_number = ''  # номер телефона для авторизации
session_file = 'account1.session'  # имя файла сессии

# создание клиента
client = TelegramClient(session_file, api_id, api_hash)

# авторизация
client.start(phone_number)

# запуск цикла обработки событий
client.run_until_disconnected()


