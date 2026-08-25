# Aqui esta toda la logica del sistema de filas.
# main.py se encarga solamente de mostrar el menu y llamar estas funciones.

from queue import PriorityQueue, Queue
import random


entradas_disponibles = 500
fila_regular = Queue()
fila_prioritaria = PriorityQueue()

# Sirven para aplicar la regla: 3 prioritarios por cada 1 regular.
prioritarios_atendidos = 0
numero_llegada = 0
numero_simulado = 1


def obtener_entradas_disponibles():
    """Devuelve cuantas entradas quedan."""
    return entradas_disponibles


def pedir_opcion_menu():
    """Pide una opcion del menu y no deja que el programa se caiga."""
    while True:
        try:
            opcion = int(input("Seleccione una opcion: "))

            if opcion >= 1 and opcion <= 5:
                return opcion

            print("Opcion invalida. Escriba un numero del 1 al 5.")
        except ValueError:
            print("Error: debe escribir un numero, no letras.")


def pedir_texto(mensaje):
    """No permite dejar vacio el nombre o la cedula."""
    while True:
        texto = input(mensaje).strip()

        if texto != "":
            return texto

        print("Este dato no puede quedar vacio.")


def pedir_cedula():
    """Acepta numeros y guiones, por ejemplo: 1-1234-5678."""
    while True:
        cedula = pedir_texto("Cedula: ")

        if cedula.replace("-", "").isdigit():
            return cedula

        print("La cedula solo puede tener numeros y guiones.")


def pedir_categoria():
    """Muestra las tres categorias posibles."""
    while True:
        print("\nCategoria del tiquete")
        print("1. Regular")
        print("2. VIP")
        print("3. Preferencial / Ley 7600")

        try:
            opcion = int(input("Seleccione una categoria: "))

            if opcion == 1:
                return "Regular"
            if opcion == 2:
                return "VIP"
            if opcion == 3:
                return "Preferencial / Ley 7600"

            print("Opcion invalida. Escriba 1, 2 o 3.")
        except ValueError:
            print("Error: debe escribir un numero.")


def agregar_a_fila(nombre, cedula, categoria):
    """Mete un comprador en la cola que le corresponde."""
    global numero_llegada

    comprador = {
        "nombre": nombre,
        "cedula": cedula,
        "categoria": categoria,
    }

    if categoria == "Regular":
        # Queue atiende en orden FIFO: primero que entra, primero que sale.
        fila_regular.put(comprador)
    else:
        if categoria == "Preferencial / Ley 7600":
            prioridad = 1
        else:
            prioridad = 2  # VIP

        # numero_llegada evita empates y conserva el orden de llegada.
        fila_prioritaria.put((prioridad, numero_llegada, comprador))
        numero_llegada += 1


def registrar_comprador():
    """Pide los datos al usuario y registra al comprador."""
    if entradas_disponibles == 0:
        print("SOLD OUT: no quedan entradas disponibles.")
        return

    print("\n--- Registrar comprador ---")
    nombre = pedir_texto("Nombre completo: ")
    cedula = pedir_cedula()
    categoria = pedir_categoria()

    agregar_a_fila(nombre, cedula, categoria)
    print("Comprador agregado a la fila " + categoria + ".")


def vaciar_colas():
    """Quita a las personas pendientes cuando se agotan las entradas."""
    cancelados = 0

    while not fila_regular.empty():
        fila_regular.get()
        cancelados += 1

    while not fila_prioritaria.empty():
        fila_prioritaria.get()
        cancelados += 1

    return cancelados


def atender_siguiente_comprador():
    """Vende una entrada siguiendo la regla de 3 prioritarios por 1 regular."""
    global entradas_disponibles
    global prioritarios_atendidos

    if entradas_disponibles == 0:
        print("SOLD OUT: no quedan entradas disponibles.")
        return

    if fila_regular.empty() and fila_prioritaria.empty():
        print("No hay compradores esperando.")
        return

    # Se atienden hasta 3 prioritarios seguidos. Luego se atiende 1 regular.
    if not fila_prioritaria.empty() and (
        fila_regular.empty() or prioritarios_atendidos < 3
    ):
        prioridad, llegada, comprador = fila_prioritaria.get()

        if prioritarios_atendidos < 3:
            prioritarios_atendidos += 1
    else:
        comprador = fila_regular.get()
        prioritarios_atendidos = 0

    entradas_disponibles -= 1

    print(
        "Entrada vendida a "
        + comprador["nombre"]
        + " - Categoria: "
        + comprador["categoria"]
        + ". Entradas restantes: "
        + str(entradas_disponibles)
    )

    # Justo al llegar a cero se dejan de vender y se vacian las filas.
    if entradas_disponibles == 0:
        cancelados = vaciar_colas()
        prioritarios_atendidos = 0
        print("SOLD OUT: entradas agotadas.")
        print("Personas retiradas de las filas: " + str(cancelados))


def mostrar_estado_filas():
    """Muestra cuantas personas esperan sin sacarlas de las colas."""
    print("\n--- Estado de las filas ---")
    print("Entradas disponibles: " + str(entradas_disponibles))
    print("Cola regular: " + str(fila_regular.qsize()) + " persona(s)")
    print("Cola prioritaria: " + str(fila_prioritaria.qsize()) + " persona(s)")


def simulacion_masiva():
    """Crea 50 compradores de prueba y los agrega automaticamente."""
    global numero_simulado

    registrados = 0

    for _ in range(50):
        if entradas_disponibles == 0:
            break

        tipo = random.randint(1, 3)

        if tipo == 1:
            categoria = "Regular"
        elif tipo == 2:
            categoria = "VIP"
        else:
            categoria = "Preferencial / Ley 7600"

        nombre = "Cliente simulado " + str(numero_simulado)
        cedula = "SIM-" + str(numero_simulado)
        agregar_a_fila(nombre, cedula, categoria)

        numero_simulado += 1
        registrados += 1

    print("Se registraron " + str(registrados) + " compradores de prueba.")
