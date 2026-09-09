import os
import logging

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

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

# cargamos las variables de entorno del archivo .env
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():
    if not TOKEN:
        raise RuntimeError("No se encontro TELEGRAM_TOKEN. Revisa tu archivo .env")

    app = ApplicationBuilder().token(TOKEN).build()

    # comandos de Persona 1, ya funcionando
    app.add_handler(CommandHandler("hola", hola))
    app.add_handler(CommandHandler("contacto", contacto))
    app.add_handler(CommandHandler("integrantes", integrantes))

    # comandos de Persona 2, 3 y 4, pendientes de implementar
    app.add_handler(CommandHandler("hora", hora))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("calcular", calcular_cmd))
    app.add_handler(CommandHandler("tabla", tabla))
    app.add_handler(CommandHandler("convertir", convertir))
    app.add_handler(CommandHandler("aleatorio", aleatorio))

    # manejo de comandos que no existen, debe ir al final
    app.add_handler(MessageHandler(filters.COMMAND, comando_desconocido))

    logging.info("Bot iniciado. Presiona Ctrl+C para detener.")
    app.run_polling()


if __name__ == "__main__":
    main()