# Este archivo solo muestra el menu y llama las funciones del sistema.

import funciones


def mostrar_menu():
    print("\n============================================")
    print("TICKET UNA - FILA VIRTUAL")
    print("Entradas disponibles: " + str(funciones.obtener_entradas_disponibles()))
    print("============================================")
    print("1. Registrar comprador en fila")
    print("2. Atender siguiente comprador")
    print("3. Mostrar estado de las filas")
    print("4. Simulacion masiva (50 compradores)")
    print("5. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = funciones.pedir_opcion_menu()

        if opcion == 1:
            funciones.registrar_comprador()
        elif opcion == 2:
            funciones.atender_siguiente_comprador()
        elif opcion == 3:
            funciones.mostrar_estado_filas()
        elif opcion == 4:
            funciones.simulacion_masiva()
        else:
            print("Programa finalizado.")
            break


if __name__ == "__main__":
    main()
