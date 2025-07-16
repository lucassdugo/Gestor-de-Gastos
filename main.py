from auxiliar import (
    agregar_movimiento,
    mostrar_movimientos,
    mostrar_totales,
    mostrar_saldo,
    definir_presupuesto,
    mostrar_presupuestos,
    eliminar_presupuestos,
    eliminar_un_registro,
    eliminar_registros,
    limpiar_pantalla
)

def menu():
    while True:
        limpiar_pantalla()
        print("=== GESTOR DE GASTOS ===")
        print("1. Registrar ingreso o gasto")
        print("2. Ver movimientos")
        print("3. Ver total de gastos por categoría")
        print("4. Ver saldo actual")
        print("5. Definir presupuesto mensual")
        print("6. Ver presupuestos mensuales")
        print("7. Eliminar todos los presupuestos")
        print("8. Eliminar un registro")
        print("9. Eliminar todos los registros")
        print("10. Salir")
        opcion = input("Elegí una opción [1-10]: ")

        if opcion == "1":
            agregar_movimiento()
        elif opcion == "2":
            mostrar_movimientos()
        elif opcion == "3":
            mostrar_totales()
        elif opcion == "4":
            mostrar_saldo()
        elif opcion == "5":
            definir_presupuesto()
        elif opcion == "6":
            mostrar_presupuestos()
        elif opcion == "7":
            eliminar_presupuestos()
        elif opcion == "8":
            eliminar_un_registro()
        elif opcion == "9":
            eliminar_registros()
        elif opcion == "10":
            print("Gracias por usar el gestor.")
            break
        else:
            print("Opción inválida.")
        input("\nPresioná ENTER para continuar...")

if __name__ == "__main__":
    menu()
