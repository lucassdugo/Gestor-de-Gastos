import csv
import os
from datetime import datetime

ARCHIVO = "gastos.csv"
PRESUPUESTO_ARCHIVO = "presupuestos.csv"
CATEGORIAS_BASE = ["Necesario", "Innecesario", "Ocio", "Otros"]

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_monto(monto_str):
    try:
        monto = float(monto_str)
        return monto if monto >= 0 else None
    except ValueError:
        return None

def obtener_categorias_dinamicas():
    categorias = set(CATEGORIAS_BASE)
    try:
        with open(ARCHIVO, newline="") as f:
            for fila in csv.reader(f):
                if len(fila) == 5:
                    categorias.add(fila[3])
    except FileNotFoundError:
        pass
    return sorted(categorias)

def formatear_monto(monto):
    base = f"{monto:,.2f}"
    return base.replace(",", "X").replace(".", ",").replace("X", ".")

def definir_presupuesto():
    descripcion = input("Descripción del gasto planificado: ")
    monto_str    = input("Monto planificado ($) sin puntos ni comas: ")
    monto = validar_monto(monto_str)
    if monto is None:
        print("Monto inválido.")
        return
    with open(PRESUPUESTO_ARCHIVO, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([descripcion, monto, monto])
    print(f"Presupuesto '{descripcion}' de ${formatear_monto(monto)} definido.")

def mostrar_presupuestos(return_list=False):
    try:
        filas = list(csv.reader(open(PRESUPUESTO_ARCHIVO, newline="")))
    except FileNotFoundError:
        filas = []
    if not filas:
        print("\nNo hay presupuestos definidos.")
        return [] if return_list else None
    print("\n=== PRESUPUESTOS MENSUALES ===")
    for idx, fila in enumerate(filas, start=1):
        if len(fila) == 3:
            desc, plan_str, rem_str = fila
            plan = float(plan_str); rem = float(rem_str)
            print(f"{idx}. {desc} | Planificado: ${formatear_monto(plan)} | A pagar: ${formatear_monto(rem)}")
        else:
            print(f"{idx}. Presupuesto incompleto omitido.")
    return filas if return_list else None

def actualizar_presupuesto_por_indice(index, pago):
    try:
        filas = list(csv.reader(open(PRESUPUESTO_ARCHIVO, newline="")))
    except FileNotFoundError:
        return
    if 0 <= index < len(filas) and len(filas[index]) == 3:
        _, plan_str, rem_str = filas[index]
        restante = max(float(rem_str) - pago, 0)
        filas[index][2] = str(restante)
        with open(PRESUPUESTO_ARCHIVO, "w", newline="") as f:
            csv.writer(f).writerows(filas)

def agregar_movimiento():
    print("Seleccione tipo de movimiento:")
    print("0. Volver al menú principal")
    print("1. Ingreso")
    print("2. Gasto")
    opt = input("Opción [0/1/2]: ")
    if opt == "0":
        return
    elif opt == "1":
        tipo = "Ingreso"
    elif opt == "2":
        tipo = "Gasto"
    else:
        print("Tipo inválido.")
        return

    presupuestos = []
    if tipo == "Gasto":
        presupuestos = mostrar_presupuestos(return_list=True)
        if presupuestos:
            print("\nSeleccioná presupuesto (ID) o 0 para descripción manual:")
            sel = input(f"ID [0-{len(presupuestos)}]: ")
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(presupuestos):
                    descripcion = presupuestos[idx][0]
                    print(f"Usando descripción: {descripcion}")
                else:
                    descripcion = input("Descripción (nueva): ")
            else:
                descripcion = input("Descripción (nueva): ")
        else:
            descripcion = input("Descripción: ")
    else:
        descripcion = input("Descripción: ")

    categorias = obtener_categorias_dinamicas()
    print("Categorías disponibles:", ", ".join(categorias))
    categoria = input("Categoría (o escribe nueva): ").capitalize()

    monto_str = input("Monto ($) sin puntos ni comas: ")
    monto = validar_monto(monto_str)
    if monto is None:
        print("Monto inválido.")
        return

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVO, "a", newline="") as f:
        csv.writer(f).writerow([fecha, tipo, descripcion, categoria, monto])
    print(f"{tipo} de ${formatear_monto(monto)} registrado bajo '{descripcion}'.")

    if tipo == "Gasto" and presupuestos and sel.isdigit() and 1 <= int(sel) <= len(presupuestos):
        actualizar_presupuesto_por_indice(int(sel)-1, monto)
        print("Presupuesto actualizado automáticamente.")

def mostrar_movimientos():
    print("\n=== LISTADO DE MOVIMIENTOS ===")
    try:
        filas = list(csv.reader(open(ARCHIVO, newline="")))
    except FileNotFoundError:
        filas = []
    if not filas:
        print("No hay movimientos registrados.")
        return
    for i, fila in enumerate(filas, start=1):
        if len(fila) == 5:
            fch, tp, desc, cat, mstr = fila
            try:
                mfmt = formatear_monto(float(mstr))
            except:
                mfmt = mstr
            print(f"{i}. {fch} | {tp} | {desc} | {cat} | ${mfmt}")
        else:
            print(f"{i}. Fila incompleta omitida.")

def mostrar_totales():
    print("\n=== TOTAL POR CATEGORÍA (Solo Gastos) ===")
    tot = {}
    try:
        for fila in csv.reader(open(ARCHIVO, newline="")):
            if len(fila) == 5 and fila[1] == "Gasto":
                cat, m = fila[3], float(fila[4])
                tot[cat] = tot.get(cat, 0) + m
    except FileNotFoundError:
        pass
    if not tot:
        print("No hay gastos registrados.")
        return
    for cat, m in tot.items():
        print(f"{cat}: ${formatear_monto(m)}")

def mostrar_saldo():
    ing = gas = 0
    try:
        for fila in csv.reader(open(ARCHIVO, newline="")):
            if len(fila) == 5:
                if fila[1] == "Ingreso":
                    ing += float(fila[4])
                elif fila[1] == "Gasto":
                    gas += float(fila[4])
    except FileNotFoundError:
        pass
    print("\n=== SALDO ===")
    print(f"Ingresos: ${formatear_monto(ing)}")
    print(f"Gastos:   ${formatear_monto(gas)}")
    print(f"Restante: ${formatear_monto(ing - gas)}")

def eliminar_presupuestos():
    resp = input("¿Eliminar *todos* los presupuestos? [s/n]: ").lower()
    if resp == 's':
        open(PRESUPUESTO_ARCHIVO, 'w').close()
        print("Todos los presupuestos han sido eliminados.")
    else:
        print("Operación cancelada.")

def eliminar_un_registro():
    try:
        filas = list(csv.reader(open(ARCHIVO, newline="")))
    except FileNotFoundError:
        filas = []
    if not filas:
        print("No hay movimientos registrados.")
        return
    for i, fila in enumerate(filas, start=1):
        if len(fila) == 5:
            fch, tp, desc, cat, mstr = fila
            try:
                mfmt = formatear_monto(float(mstr))
            except:
                mfmt = mstr
            print(f"{i}. {fch} | {tp} | {desc} | {cat} | ${mfmt}")
        else:
            print(f"{i}. Fila incompleta omitida.")
    sel = input("IDs a eliminar (separados por comas): ")
    ids = sorted({int(s) for s in sel.split(",") if s.strip().isdigit()}, reverse=True)
    if not ids:
        print("No ingresaste IDs válidos.")
        return
    if any(n < 1 or n > len(filas) for n in ids):
        print("Algún ID fuera de rango.")
        return
    elim = []
    for n in ids:
        elim.append(filas.pop(n - 1))
    with open(ARCHIVO, "w", newline="") as f:
        csv.writer(f).writerows(filas)
    print("Registros eliminados:")
    for fila in elim:
        fch, tp, desc, cat, mstr = fila
        try:
            mfmt = formatear_monto(float(mstr))
        except:
            mfmt = mstr
        print(f"- {fch} | {tp} | {desc} | {cat} | ${mfmt}")

def eliminar_registros():
    resp = input("¿Eliminar *todos* los registros? [s/n]: ").lower()
    if resp == 's':
        open(ARCHIVO, 'w').close()
        print("Todos los registros han sido eliminados.")
    else:
        print("Operación cancelada.")
