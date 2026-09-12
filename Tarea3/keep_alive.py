import os
import threading

from flask import Flask

# Servidor para mantener el bot activo en Render
# Render duerme el servicio si no recibe peticiones HTTP.

app = Flask(__name__)


@app.route("/")
def home():
    return "Bot de Telegram activo."


def _run():
    puerto = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=puerto)


def keep_alive():
    hilo = threading.Thread(target=_run, daemon=True)
    hilo.start()
