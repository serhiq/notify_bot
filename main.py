from telethon import TelegramClient, events
from telethon.errors import SessionExpiredError
from telethon.errors.rpcerrorlist import PhoneNumberBannedError

api_id = "YOU_API_ID"
api_hash = 'API_HASH'
bot_token = 'BOT_TOKEN'

bot_client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# список аккаунтов
accounts = [
    {'phone': 'YOU_PHONE', 'session_file': 'account1.session'},
]

# список идентификаторов аккаунтов, на которые будут приходить уведомления
notify_account_ids = [11111111111]

# список клиентов Telegram
clients = []

# создаем клиентов Telegram и добавляем обработчики событий для каждого аккаунта
for i, account in enumerate(accounts):
    client = TelegramClient(account['session_file'], api_id, api_hash)
    clients.append(client)

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        try:
            print(f"New message from {account['phone']}: {event.message.message}")
            notify_message = f"New message from {account['phone']}: {event.message.message}"
            notify_account_id = notify_account_ids[i]
        # обрабатываем полученное сообщение и отправляем уведомление через Телеграм-бот
        except SessionExpiredError:
            # обработка ошибки, если сессия аккаунта пользователя истекла
            print('Сессия пользователя истекла')
            notify_message = 'Сессия пользователя истекла'
        except PhoneNumberBannedError:
            # обработка ошибки, если аккаунт пользователя заблокирован
            print('Аккаунт пользователя заблокирован')
            notify_message = 'Аккаунт пользователя заблокирован'
        except Exception as e:
            # обработка других ошибок
            print(f'Произошла ошибка: {e}')
            notify_message = f'Произошла ошибка: {e}'
        finally:
            if notify_message:
                await bot_client.send_message(notify_account_id, notify_message)


    client.start()

# запускаем клиентский цикл для всех аккаунтов
for client in clients:
    client.run_until_disconnected()
