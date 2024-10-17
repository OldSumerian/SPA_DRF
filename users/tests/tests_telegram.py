from rest_framework.test import APITestCase
import responses

from config.settings import TELEGRAM_API_URL, TELEGRAM_BOT_TOKEN
from users.models import User
from users.services_telegram import (
    get_chat_id,
    sent_notification_in_telegram,
    update_chat_id,
)


class TestCase(APITestCase):

    @responses.activate
    def test_get_chat_id_OK(self):
        username = "OldSumerian"

        body = (
            '{"ok":true,"result":[{"update_id":24152962,"message":'
            '{"message_id":3,"from":{"id":111111111,"is_bot":false,'
            '"first_name":"Sergey","last_name":"Shemerov","username":'
            '"OldSumerian","language_code":"ru"},"chat":'
            '{"id":111111111,"first_name":"Sergey","last_name":'
            '"Shemerov","username":"OldSumerian","type":"private"},'
            '"date":1725895346,"text":"sddds"}}]}'
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
                "body": body,
                "status": 200,
                "content_type": "application/json",
            }
        )

        self.assertEqual(get_chat_id(username), 111111111)

    @responses.activate
    def test_get_chat_id_empty(self):
        username = "OldSumerian"
        body = '{"ok":true,"result":[]}'

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
                "body": body,
                "status": 200,
                "content_type": "application/json",
            }
        )

        self.assertEqual(get_chat_id(username), 0)

    @responses.activate
    def test_get_chat_id_user_not_found(self):
        username = "NewUser"
        body = (
            '{"ok":true,"result":[{"update_id":24152962,"message":'
            '{"message_id":3,"from":{"id":111111111,"is_bot":false,'
            '"first_name":"Ivan","last_name":"Ivanov","username":'
            '"NewUser","language_code":"ru"},"chat":'
            '{"id":111111111,"first_name":"Ivan","last_name":'
            '"Ivanov","username":"NewUser","type":"private"},'
            '"date":1725895346,"text":"sddds"}}]}'
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
                "body": body,
                "status": 200,
                "content_type": "application/json",
            }
        )

        self.assertEqual(get_chat_id(username), 0)

    @responses.activate
    def test_get_chat_id_not_ok(self):
        username = "ChurilovEvgeny"
        body = '{"ok":true,"result":[]}'

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
                "body": body,
                "status": 404,
                "content_type": "application/json",
            }
        )

        self.assertEqual(get_chat_id(username), 0)

    @responses.activate
    def test_send_message_OK(self):
        chat_id = 111111111
        body = '{"ok":true}'

        responses.add(
            **{
                "method": responses.POST,
                "url": f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                "body": body,
                "status": 200,
                "content_type": "application/json",
            }
        )

        self.assertTrue(sent_notification_in_telegram("message", chat_id))

    @responses.activate
    def test_send_message_no_chat_id(self):
        chat_id = 0

        self.assertFalse(sent_notification_in_telegram("message", chat_id))

    @responses.activate
    def test_send_message_fail(self):
        chat_id = 111111111
        body = '{"ok":true}'

        responses.add(
            **{
                "method": responses.POST,
                "url": f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                "body": body,
                "status": 403,
                "content_type": "application/json",
            }
        )

        self.assertFalse(sent_notification_in_telegram("message", chat_id))

    @responses.activate
    def test_update_chat_id_exists(self):
        user = User.objects.create(
            email="user@my.ru", tg_name="ChurilovEvgeny", tg_chat_id=1
        )
        update_chat_id(user)
        self.assertEqual(user.tg_chat_id, 1)

    @responses.activate
    def test_update_chat_id_new_chat_id(self):
        user = User.objects.create(
            email="user@my.ru", tg_name="ChurilovEvgeny", tg_chat_id=0
        )

        body = (
            '{"ok":true,"result":[{"update_id":24152962,"message":'
            '{"message_id":3,"from":{"id":111111111,"is_bot":false,'
            '"first_name":"Evgeny","last_name":"Churilov","username":'
            '"ChurilovEvgeny","language_code":"ru"},"chat":'
            '{"id":111111111,"first_name":"Evgeny","last_name":'
            '"Churilov","username":"ChurilovEvgeny","type":"private"},'
            '"date":1725895346,"text":"sddds"}}]}'
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
                "body": body,
                "status": 200,
                "content_type": "application/json",
            }
        )

        update_chat_id(user)
        self.assertEqual(user.tg_chat_id, 111111111)
