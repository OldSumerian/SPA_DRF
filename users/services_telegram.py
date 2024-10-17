from http import HTTPStatus

import requests

from config.settings import TELEGRAM_API_URL, TELEGRAM_BOT_TOKEN
from users.models import User


def get_chat_id(username):
    """
    Возвращает ID чата по имени пользователя в Telegram.
    """
    response = requests.get(
        f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
    )

    if response.status_code == HTTPStatus.OK:
        chat_data = response.json()
        if chat_data["result"]:
            for chat in chat_data["result"]:
                if chat["message"]["from"]["username"] == username:
                    return chat["message"]["chat"]["id"]
            print("Чат с данным пользователем не существует")
            return 0
        else:
            print("Чат пуст")
            return 0
    else:
        print(f"Error: {response.status_code}")
        return 0


def update_chat_id(user: User):
    # Если чат ид не нулевой, то ничего не делаем
    if user.tg_chat_id:
        return

    # Получаем ID чата из Telegram
    chat_id = get_chat_id(user.tg_name)
    if chat_id:
        user.tg_chat_id = chat_id
        user.save()


def sent_notification_in_telegram(message, chat_id) -> bool:
    """
    Отправляет сообщение в чат с указанным ID чата.
    """
    if not chat_id:
        print("Chat id не указан")
        return False

    response = requests.post(
        f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        params={"chat_id": chat_id, "text": message},
    )

    if response.status_code == HTTPStatus.OK:
        print("Сообщение успешно отправлено")
        return True
    else:
        print(f"Error: {response.status_code}")
        return False
