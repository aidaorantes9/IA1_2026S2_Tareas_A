# Tarea 2 - Backend
# API REST que conecta Flask con Prolog usando PySwip
# ================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog

app = Flask(__name__)

# habilito CORS para que el navegador (frontend) pueda pedirle datos a esta API
CORS(app)

# cargo el archivo .pl una sola vez cuando arranca el servidor
prolog = Prolog()
prolog.consult("inventario.pl")


@app.route("/inventario", methods=["GET"])
def obtener_inventario():
    # tomo el item que el usuario mando por query string, ej: /inventario?item=espada
    item_buscado = request.args.get("item")

    if not item_buscado:
        return jsonify({"error": "Falta el parametro 'item' en la peticion"}), 400

    # arma la consulta como texto y la manda a Prolog
    consulta = f"procesar_inventario({item_buscado}, TotalItems, InventarioInvertido, InventarioUnico, InventarioOrdenado)"
    resultados = list(prolog.query(consulta))

    # esto imprime en la consola del backend lo que Prolog fue mostrando (writeln)
    # ya se ve solo porque PySwip manda esa salida directo a la terminal

    if not resultados:
        # si no hubo resultados es porque el item no existe en el inventario
        return jsonify({"error": f"El item '{item_buscado}' no existe en el inventario"}), 404

    r = resultados[0]

    # armo el diccionario que se convierte en JSON, convirtiendo cada item a texto
    respuesta = {
        "total_items": r["TotalItems"],
        "inventario_invertido": [str(x) for x in r["InventarioInvertido"]],
        "inventario_unico": [str(x) for x in r["InventarioUnico"]],
        "inventario_ordenado": [str(x) for x in r["InventarioOrdenado"]],
    }

    return jsonify(respuesta)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
