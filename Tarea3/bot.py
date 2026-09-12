import os
import time
import logging
import asyncio

from dotenv import load_dotenv

from telegram_api import TelegramClient, Update, Context, Message, User, CallbackQuery

from commands import (
    hola,
    contacto,
    integrantes,
    hora,
    ayuda,
    calcular_cmd,
    aleatorio,
    tabla,
    convertir,
    comando_desconocido,
)
from menu import menu, menu_callback
from keep_alive import keep_alive

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

COMANDOS = {
    "/hola": hola,
    "/contacto": contacto,
    "/integrantes": integrantes,
    "/hora": hora,
    "/ayuda": ayuda,
    "/menu": menu,
    "/calcular": calcular_cmd,
    "/tabla": tabla,
    "/convertir": convertir,
    "/aleatorio": aleatorio,
}


def _extraer_chat_id(actualizacion):
    if "message" in actualizacion:
        return actualizacion["message"]["chat"]["id"]
    if "callback_query" in actualizacion:
        return actualizacion["callback_query"]["message"]["chat"]["id"]
    return None


def procesar_mensaje(cliente, mensaje):
    texto = mensaje.get("text", "")
    if not texto.startswith("/"):
        return

    partes = texto.strip().split()
    comando = partes[0].split("@")[0]  # soporta /comando@nombre_del_bot
    args = partes[1:]

    chat_id = mensaje["chat"]["id"]
    remitente = mensaje.get("from", {})

    update = Update(
        message=Message(cliente, chat_id),
        effective_user=User(remitente.get("first_name"), remitente.get("username")),
    )
    context = Context(args=args)

    funcion = COMANDOS.get(comando, comando_desconocido)
    asyncio.run(funcion(update, context))


def procesar_callback(cliente, callback_query):
    chat_id = callback_query["message"]["chat"]["id"]
    remitente = callback_query.get("from", {})

    mensaje_respuesta = Message(cliente, chat_id)
    callback = CallbackQuery(
        cliente,
        callback_query["id"],
        callback_query.get("data", ""),
        mensaje_respuesta,
    )
    update = Update(
        effective_user=User(remitente.get("first_name"), remitente.get("username")),
        callback_query=callback,
    )
    context = Context()

    asyncio.run(menu_callback(update, context))


# si al procesar una actualizacion ocurre cualquier excepcion, se registra
# y se avisa al usuario en vez de dejar que el bot se detenga
def procesar_actualizacion(cliente, actualizacion):
    try:
        if "message" in actualizacion:
            procesar_mensaje(cliente, actualizacion["message"])
        elif "callback_query" in actualizacion:
            procesar_callback(cliente, actualizacion["callback_query"])
    except Exception:
        logging.exception("Excepcion no manejada al procesar una actualizacion")
        chat_id = _extraer_chat_id(actualizacion)
        if chat_id is not None:
            try:
                cliente.send_message(
                    chat_id,
                    "Ocurrio un error inesperado al procesar tu solicitud. Intenta nuevamente.",
                )
            except Exception:
                logging.exception("No se pudo notificar el error al usuario")


def main():
    if not TOKEN:
        raise RuntimeError("No se encontro TELEGRAM_TOKEN. Revisa tu archivo .env")

    cliente = TelegramClient(TOKEN)
    cliente.delete_webhook()

    # en Render se define la variable PORT automaticamente; si existe,
    # levantamos el servidor de keep-alive para que el servicio no se
    # duerma por inactividad. En local (sin PORT) no se levanta.
    if os.getenv("PORT"):
        keep_alive()

    logging.info("Bot iniciado. Presiona Ctrl+C para detener.")

    offset = None
    while True:
        try:
            actualizaciones = cliente.get_updates(offset=offset, timeout=30)
        except Exception:
            logging.exception("Error al consultar getUpdates, reintentando en unos segundos...")
            time.sleep(3)
            continue

        for actualizacion in actualizaciones:
            offset = actualizacion["update_id"] + 1
            procesar_actualizacion(cliente, actualizacion)


if __name__ == "__main__":
    main()