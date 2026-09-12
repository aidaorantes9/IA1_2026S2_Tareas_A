"""
Cliente propio y minimo para la API de Telegram, usando unicamente la
libreria 'requests' (sin ninguna libreria de bots como python-telegram-bot).

Expone clases con la misma forma (duck typing) que usan commands.py y
menu.py -Update, ContextTypes, InlineKeyboardButton, InlineKeyboardMarkup-
para que la logica de cada comando no tenga que cambiar.
"""

import requests


class _DefaultType:
    """Marcador usado solo como anotacion de tipo (ver Context mas abajo)."""


class ContextTypes:
    DEFAULT_TYPE = _DefaultType


class InlineKeyboardButton:
    def __init__(self, text, callback_data):
        self.text = text
        self.callback_data = callback_data

    def to_dict(self):
        return {"text": self.text, "callback_data": self.callback_data}


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard):
        self.inline_keyboard = inline_keyboard

    def to_dict(self):
        return {
            "inline_keyboard": [
                [boton.to_dict() for boton in fila] for fila in self.inline_keyboard
            ]
        }


class TelegramClient:
    def __init__(self, token):
        self.base_url = f"https://api.telegram.org/bot{token}"

    def get_me(self):
        return requests.get(f"{self.base_url}/getMe", timeout=15).json()

    def delete_webhook(self):
        return requests.post(f"{self.base_url}/deleteWebhook", timeout=15).json()

    def get_updates(self, offset=None, timeout=30):
        params = {"timeout": timeout}
        if offset is not None:
            params["offset"] = offset
        respuesta = requests.get(
            f"{self.base_url}/getUpdates", params=params, timeout=timeout + 10
        )
        respuesta.raise_for_status()
        return respuesta.json().get("result", [])

    def send_message(self, chat_id, texto, reply_markup=None):
        payload = {"chat_id": chat_id, "text": texto}
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup.to_dict()
        respuesta = requests.post(f"{self.base_url}/sendMessage", json=payload, timeout=15)
        respuesta.raise_for_status()
        return respuesta.json()

    def answer_callback_query(self, callback_query_id):
        respuesta = requests.post(
            f"{self.base_url}/answerCallbackQuery",
            json={"callback_query_id": callback_query_id},
            timeout=15,
        )
        respuesta.raise_for_status()
        return respuesta.json()


class Message:
    def __init__(self, cliente: TelegramClient, chat_id):
        self._cliente = cliente
        self.chat_id = chat_id

    async def reply_text(self, texto, reply_markup=None):
        self._cliente.send_message(self.chat_id, texto, reply_markup=reply_markup)


class User:
    def __init__(self, first_name=None, username=None):
        self.first_name = first_name
        self.username = username


class CallbackQuery:
    def __init__(self, cliente: TelegramClient, callback_query_id, data, message: Message):
        self._cliente = cliente
        self.id = callback_query_id
        self.data = data
        self.message = message

    async def answer(self):
        self._cliente.answer_callback_query(self.id)


class Update:
    def __init__(self, message: Message = None, effective_user: User = None, callback_query: CallbackQuery = None):
        self.message = message
        self.effective_message = message if message is not None else (
            callback_query.message if callback_query is not None else None
        )
        self.effective_user = effective_user
        self.callback_query = callback_query


class Context:
    def __init__(self, args=None):
        self.args = args or []
