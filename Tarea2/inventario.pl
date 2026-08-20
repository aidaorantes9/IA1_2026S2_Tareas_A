% ================================
% Motor de inferencia
% Inventario de un RPG en Prolog
% ================================

% --- Hechos ---

% Items principales del aventurero (nota: "pocion" esta repetido a proposito)
inventario_principal([espada, escudo, pocion, pocion]).

% Items secundarios del aventurero (3 items distintos)
inventario_secundario([daga, cuerda, antorcha]).


% --- Regla recursiva para recorrer e imprimir el inventario ---

% Caso base: si la lista esta vacia ya no hay nada que imprimir
mostrar_inventario([]).

% Caso recursivo: separo la lista en Cabeza (primer item) y Cola (resto)
% imprimo la Cabeza y luego llamo la funcion otra vez con la Cola
mostrar_inventario([Cabeza|Cola]) :-
    writeln(Cabeza),
    mostrar_inventario(Cola).


% --- Regla principal ---
% procesar_inventario/5: recibe el ItemBuscado y devuelve 4 variables
% usando los 6 metodos nativos pedidos: append, length, member,
% reverse, sort y msort
procesar_inventario(ItemBuscado, TotalItems, InventarioInvertido, InventarioUnico, InventarioOrdenado) :-
    inventario_principal(Principal),
    inventario_secundario(Secundario),

    % append/3 (aridad 3): une las dos listas en una sola
    append(Principal, Secundario, InventarioGeneral),

    % length/2 (aridad 2): cuenta cuantos items hay en total
    length(InventarioGeneral, TotalItems),

    % member/2 (aridad 2): verifica que el item buscado si esta en la lista
    % si no esta, la consulta falla (por eso hay que buscar un item que exista)
    member(ItemBuscado, InventarioGeneral),

    % reverse/2 (aridad 2): invierte el orden de la lista
    reverse(InventarioGeneral, InventarioInvertido),

    % sort/2 (aridad 2): ordena y ademas quita los duplicados
    sort(InventarioGeneral, InventarioUnico),

    % msort/2 (aridad 2): ordena pero SI deja los duplicados
    msort(InventarioGeneral, InventarioOrdenado),

    % ultimo paso: imprimo todo el inventario general de forma recursiva
    mostrar_inventario(InventarioGeneral).
