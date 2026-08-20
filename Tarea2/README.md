# Tarea 2 - Inventario RPG (Prolog + Python + HTML)

## Descripción
Sistema que maneja el inventario de un aventurero de RPG. La lógica de listas
está hecha en Prolog, un backend en Python (Flask) conecta ese motor con una
API REST, y un frontend en HTML/JS permite buscar un item y ver los resultados.

## Flujo del sistema
1. El usuario escribe un item en el input del frontend (`index.html`) y presiona "Buscar".
2. El frontend hace un `fetch` con GET a `http://127.0.0.1:5000/inventario?item=NOMBRE`.
3. Flask (`app.py`) recibe la petición, arma la consulta y se la manda a Prolog usando PySwip.
4. Prolog (`inventario.pl`) ejecuta `procesar_inventario/5`:
   - Une los inventarios principal y secundario con `append`.
   - Cuenta los items con `length`.
   - Verifica que el item exista con `member`.
   - Genera la lista invertida con `reverse`.
   - Genera la lista sin duplicados con `sort`.
   - Genera la lista ordenada con duplicados con `msort`.
   - Imprime todo el inventario de forma recursiva en la consola del backend con `mostrar_inventario/1`.
5. Flask toma esas variables unificadas y las regresa como JSON.
6. El frontend recibe el JSON y lo muestra en pantalla.

## Cómo correrlo

### 1. Prolog
No hace falta correrlo aparte, Flask lo carga automáticamente.

### 2. Backend
```bash
pip install flask flask-cors pyswip
python app.py
```
Esto levanta el servidor en `http://127.0.0.1:5000`

### 3. Frontend
Abrir el archivo `index.html` directamente en el navegador (doble click) o con
Live Server. Escribir un item que exista (ej: `espada`, `escudo`, `pocion`,
`daga`, `cuerda`, `antorcha`) y presionar Buscar.

## Estructura de archivos
- `inventario.pl` -> lógica de Prolog (hechos, recursividad, métodos nativos)
- `app.py` -> backend Flask + PySwip + CORS
- `index.html` -> frontend con formulario y fetch
- `README.md` -> este archivo

## Capturas

### Frontend (navegador) mostrando el resultado de una consulta exitosa
![Resultado en navegador](/Tarea2/imagenes/navegador.png)

### Consola del backend mostrando la impresión recursiva de Prolog
![Consola del backend](/Tarea2/imagenes/terminal.png)