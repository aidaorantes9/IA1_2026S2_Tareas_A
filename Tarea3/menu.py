from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from commands import hola, contacto, integrantes, hora, ayuda

# comandos que no reciben parametros: el boton ejecuta el comando directamente
COMANDOS_DIRECTOS = {
    "menu_hola": hola,
    "menu_hora": hora,
    "menu_contacto": contacto,
    "menu_integrantes": integrantes,
    "menu_ayuda": ayuda,
}

# comandos que reciben parametros: el boton solo muestra como usarlos
COMANDOS_CON_PARAMETROS = {
    "menu_calcular": (
        "/calcular <numero1> <operador> <numero2>\n"
        "Operadores validos: +  -  *  /\n"
        "Ejemplo: /calcular 5 + 3"
    ),
    "menu_tabla": (
        "/tabla <numero>\n"
        "Ejemplo: /tabla 7"
    ),
    "menu_convertir": (
        "/convertir <cantidad> <unidad_origen> <unidad_destino>\n"
        "Unidades soportadas: cm, m, km, mi, ft\n"
        "Ejemplo: /convertir 10 km mi"
    ),
    "menu_aleatorio": (
        "/aleatorio <min> <max>\n"
        "Ejemplo: /aleatorio 1 100"
    ),
}


def _construir_teclado() -> InlineKeyboardMarkup:
    botones = [
        [
            InlineKeyboardButton("Hola", callback_data="menu_hola"),
            InlineKeyboardButton("Hora", callback_data="menu_hora"),
        ],
        [
            InlineKeyboardButton("Contacto", callback_data="menu_contacto"),
            InlineKeyboardButton("Integrantes", callback_data="menu_integrantes"),
        ],
        [
            InlineKeyboardButton("Calcular", callback_data="menu_calcular"),
            InlineKeyboardButton("Tabla de multiplicar", callback_data="menu_tabla"),
        ],
        [
            InlineKeyboardButton("Convertir unidades", callback_data="menu_convertir"),
            InlineKeyboardButton("Numero aleatorio", callback_data="menu_aleatorio"),
        ],
        [InlineKeyboardButton("Ayuda", callback_data="menu_ayuda")],
    ]
    return InlineKeyboardMarkup(botones)


# Comando /menu
# Muestra un menu interactivo utilizando botones de Telegram
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "Elige una opcion para ver que puede hacer el bot:"
    await update.effective_message.reply_text(mensaje, reply_markup=_construir_teclado())


# Maneja el click de cualquier boton del menu
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    opcion = query.data

    if opcion in COMANDOS_DIRECTOS:
        funcion = COMANDOS_DIRECTOS[opcion]
        await funcion(update, context)
        return

    if opcion in COMANDOS_CON_PARAMETROS:
        instrucciones = COMANDOS_CON_PARAMETROS[opcion]
        await query.message.reply_text(
            "Este comando necesita parametros, usalo asi:\n\n" + instrucciones
        )
        return

    await query.message.reply_text("Opcion no reconocida. Usa /menu para volver a intentar.")
