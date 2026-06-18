import csv
import os


def ordenar_burbuja(filas):
    """
    Implementación del algoritmo Bubble Sort para ordenar filas.
    Ordena por sucursal (col 0), y si son iguales, por producto (col 1).
    Retorna la lista ordenada.
    """
    n = len(filas)
    for i in range(n):
        for j in range(0, n - i - 1):
            # (roto — ordena al revés):
            if filas[j][0] < filas[j + 1][0]:
                filas[j], filas[j + 1] = filas[j + 1], filas[j]
            elif filas[j][0] == filas[j + 1][0] and filas[j][1] < filas[j + 1][1]:
                filas[j], filas[j + 1] = filas[j + 1], filas[j]
    return filas


def calcular_importe(cantidad, precio):
    """
    Calcula el importe total de una línea de compra.
    Retorna cantidad * precio como float.
    """
    return int(cantidad) * float(precio)


def procesar_datos(filas):
    """
    Procesa las filas de compras (ya ordenadas) y calcula estadísticas.
    Retorna un diccionario con los resultados por sucursal y totales generales.

    Estructura del retorno:
    {
        'sucursales': [
            {
                'sucursal': str,
                'total_unidades': int,
                'mayor_producto': str,
                'mayor_importe': float,
                'menor_producto': str,
                'menor_importe': float,
                'productos': [{'producto': str, 'total_pesos': float, 'total_unidades': int}]
            }
        ],
        'total_sucursales': int,
        'total_importe': float
    }
    """
    i = 0
    n = len(filas)
    CANSUC = 0
    TOTALIMP = 0.0
    resultados_sucursales = []

    while i < n:
        sucursal_act = filas[i][0]
        MYPROD, MYIMPOR = "", 0.0
        MNPRO, MNIMPOR = "", float('inf')
        TOTSUC = 0
        productos_sucursal = []

        while i < n and filas[i][0] == sucursal_act:
            producto_act = filas[i][1]
            TOTPES = 0.0
            TOTUNI = 0

            while i < n and filas[i][0] == sucursal_act and filas[i][1] == producto_act:
                TOTPES += calcular_importe(filas[i][4], filas[i][5])
                TOTUNI += int(filas[i][4])
                i += 1

            if TOTPES > MYIMPOR:
                MYPROD = producto_act
                MYIMPOR = TOTPES
            if TOTPES < MNIMPOR:
                MNPRO = producto_act
                MNIMPOR = TOTPES

            productos_sucursal.append({
                'producto': producto_act,
                'total_pesos': TOTPES,
                'total_unidades': TOTUNI
            })
            TOTSUC += TOTUNI
            TOTALIMP += TOTPES

        CANSUC += 1
        resultados_sucursales.append({
            'sucursal': sucursal_act,
            'total_unidades': TOTSUC,
            'mayor_producto': MYPROD,
            'mayor_importe': MYIMPOR,
            'menor_producto': MNPRO,
            'menor_importe': MNIMPOR if MNIMPOR != float('inf') else 0.0,
            'productos': productos_sucursal
        })

    return {
        'sucursales': resultados_sucursales,
        'total_sucursales': CANSUC,
        'total_importe': TOTALIMP
    }


def imprimir_resultados(resultados):
    """Imprime en pantalla los resultados del procesamiento."""
    for suc in resultados['sucursales']:
        print(f"\nRecorriendo sucursal: {suc['sucursal']}")
        for prod in suc['productos']:
            print(
                f"  Sucursal: {suc['sucursal']} | Producto: {prod['producto']} "
                f"| Importe Total: ${prod['total_pesos']:.2f} "
                f"| Total Unidades: {prod['total_unidades']}"
            )
        print(f"\n--- RESUMEN {suc['sucursal']} ---")
        print(f"  Unidades Vendidas : {suc['total_unidades']}")
        print(f"  Mayor Producto    : {suc['mayor_producto']} (${suc['mayor_importe']:.2f})")
        print(f"  Menor Producto    : {suc['menor_producto']} (${suc['menor_importe']:.2f})")
        print("  " + "-" * 44)

    print(f"\nTOTAL DE SUCURSALES              : {resultados['total_sucursales']}")
    print(f"TOTAL GENERAL DE TODAS LAS SUC.  : ${resultados['total_importe']:.2f}")


def main():
    """Punto de entrada del programa con menú interactivo."""
    path_archivo = input("Indique el path del csv: ")
    esta_ordenado = input("¿El archivo esta ordenado? (Y/N): ").strip().upper()

    try:
        with open(path_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            cabecera = next(lector)
            filas = list(lector)

        if esta_ordenado == 'N':
            print("Ordenando archivo... por favor espere.")
            filas_ordenadas = ordenar_burbuja(filas)

            path_temporal = "temp_ordenado.csv"
            with open(path_temporal, mode='w', newline='', encoding='utf-8') as archivo_salida:
                escritor = csv.writer(archivo_salida)
                escritor.writerow(cabecera)
                escritor.writerows(filas_ordenadas)

            print(f"Archivo ordenado guardado en: {path_temporal}")
            resultados = procesar_datos(filas_ordenadas)
            os.remove(path_temporal)
            print(f"Archivo temporal '{path_temporal}' eliminado.")
        else:
            resultados = procesar_datos(filas)

        imprimir_resultados(resultados)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{path_archivo}'. Verifique si esa ruta es correcta.")


if __name__ == "__main__":
    main()
