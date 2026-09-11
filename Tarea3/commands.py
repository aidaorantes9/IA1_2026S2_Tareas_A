from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import ContextTypes

# Guatemala no usa horario de verano, por lo que la zona horaria es fija
ZONA_HORARIA_GT = ZoneInfo("America/Guatemala")

# =========================================================
# PERSONA 1: comandos basicos de informacion
# =========================================================

# Comando /hola
# Este comando saluda al usuario usando su nombre de Telegram
async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # obtenemos el nombre del usuario que escribio el comando
    nombre = update.effective_user.first_name or update.effective_user.username or "usuario"

    # le enviamos el saludo de vuelta
    mensaje = "Hola, " + nombre + ". Bienvenido al bot del curso."
    await update.message.reply_text(mensaje)


# Comando /contacto
# Este comando muestra la informacion de contacto del grupo
async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "Informacion de contacto:\n"
        "Somos el grupo numero 5 del laboratorio de Inteligencia Artificial 1\n"
        "GitHub: https://github.com/aidaorantes9/IA1_2026S2_Tareas_A"
    )
    await update.message.reply_text(mensaje)


# Comando /integrantes
# Este comando muestra el nombre y carnet de cada integrante del grupo
async def integrantes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = (
        "Integrantes del grupo:\n"
        "- Estefania Anaide Mazariegos Munoz - Carnet 202300547\n"
        "- Kenneth Isai Aquino Ortiz - Carnet 202100678\n"
        "- Henry David Quel Santos - Carnet 202004071\n"
        "- Aida Alejandra Mansilla Orantes - Carnet 202100239\n"
        "- Andrea Alejandra Perez Sandoval - Carnet 202201136"
    )
    await update.message.reply_text(lista)


# =========================================================
# PERSONA 2: comandos dinamicos y ayuda
# =========================================================

# Comando /hora
# Muestra la fecha y hora actual de forma dinamica (zona horaria de Guatemala)
async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ahora = datetime.now(ZONA_HORARIA_GT)
    mensaje = (
        "Fecha y hora actual en Guatemala:\n"
        + ahora.strftime("%d/%m/%Y %H:%M:%S")
    )
    await update.effective_message.reply_text(mensaje)


# Lista central de comandos usada por /ayuda y como referencia para /menu
LISTA_COMANDOS = [
    ("/hola", "Saluda al usuario utilizando su nombre de Telegram."),
    ("/hora", "Muestra la fecha y hora actual de Guatemala."),
    ("/contacto", "Muestra la informacion de contacto del grupo."),
    ("/integrantes", "Muestra el nombre y carnet de los integrantes del grupo."),
    ("/ayuda", "Muestra esta lista de comandos disponibles."),
    ("/menu", "Muestra un menu interactivo con botones."),
    ("/calcular <numero1> <operador> <numero2>", "Suma, resta, multiplica o divide dos numeros."),
    ("/tabla <numero>", "Muestra la tabla de multiplicar del 1 al 10."),
    ("/convertir <cantidad> <unidad_origen> <unidad_destino>", "Convierte entre cm, m, km, mi y ft."),
    ("/aleatorio <min> <max>", "Genera un numero entero aleatorio dentro del rango indicado."),
]


# Comando /ayuda
# Muestra la lista de comandos disponibles y una breve descripcion de cada uno
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lineas = ["Comandos disponibles:"]
    for comando, descripcion in LISTA_COMANDOS:
        lineas.append(comando + " - " + descripcion)
    mensaje = "\n".join(lineas)
    await update.effective_message.reply_text(mensaje)


# =========================================================
# PERSONA 3: calculadora, aleatorio y validaciones
# =========================================================

async def calcular_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO Persona 3: leer numero1, operador, numero2 y validar
    pass


async def aleatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO Persona 3: generar numero aleatorio entre min y max
    pass


# =========================================================
# PERSONA 4: tabla de multiplicar y conversor de unidades
# =========================================================

async def tabla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO Persona 4: mostrar tabla de multiplicar del 1 al 10
    pass


async def convertir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO Persona 4: convertir entre cm, m, km, mi, ft
    pass


# =========================================================
# Manejo de comandos inexistentes
# =========================================================

async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "No reconozco ese comando. Usa /ayuda para ver la lista de comandos disponibles."
    )

