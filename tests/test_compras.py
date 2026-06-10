"""
Tests unitarios para el sistema de procesamiento de compras del supermercado.
Cubre: ordenar_burbuja, calcular_importe, procesar_datos.
"""
import pytest
import sys
import os

# Asegura que Python encuentre compras.py desde cualquier entorno
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compras import ordenar_burbuja, calcular_importe, procesar_datos


# ---------------------------------------------------------------------------
# Datos de prueba reutilizables
# ---------------------------------------------------------------------------

FILAS_ORDENADAS = [
    ['S01', 'P001', '2024-01-01', 'PROV1', '10', '5.50'],
    ['S01', 'P001', '2024-01-02', 'PROV2', '5',  '6.00'],
    ['S01', 'P002', '2024-01-01', 'PROV1', '20', '3.00'],
    ['S02', 'P001', '2024-01-01', 'PROV1', '15', '5.50'],
    ['S02', 'P003', '2024-01-01', 'PROV2', '8',  '12.00'],
]
# S01-P001: 10*5.50 + 5*6.00 = 55 + 30 = 85.00  (15 unidades)
# S01-P002: 20*3.00 = 60.00                       (20 unidades)
# S02-P001: 15*5.50 = 82.50                       (15 unidades)
# S02-P003: 8*12.00 = 96.00                       ( 8 unidades)
# TOTAL IMPORTE: 323.50

FILAS_DESORDENADAS = [
    ['S02', 'P001', '2024-01-01', 'PROV1', '15', '5.50'],
    ['S01', 'P002', '2024-01-01', 'PROV1', '20', '3.00'],
    ['S01', 'P001', '2024-01-01', 'PROV1', '10', '5.50'],
    ['S02', 'P003', '2024-01-01', 'PROV2', '8',  '12.00'],
    ['S01', 'P001', '2024-01-02', 'PROV2', '5',  '6.00'],
]


# ---------------------------------------------------------------------------
# Tests: ordenar_burbuja
# ---------------------------------------------------------------------------

class TestOrdenarBurbuja:

    def test_ordena_por_sucursal(self):
        """La primera fila del resultado debe ser la de menor sucursal."""
        resultado = ordenar_burbuja(FILAS_DESORDENADAS.copy())
        assert resultado[0][0] == 'S01', "La primera sucursal ordenada debe ser S01"

    def test_ultima_fila_es_mayor_sucursal(self):
        """La última fila del resultado debe ser la de mayor sucursal."""
        resultado = ordenar_burbuja(FILAS_DESORDENADAS.copy())
        assert resultado[-1][0] == 'S02', "La última sucursal ordenada debe ser S02"

    def test_archivo_ya_ordenado_no_cambia(self):
        """Un archivo ya ordenado no debe modificarse."""
        copia = [fila[:] for fila in FILAS_ORDENADAS]
        resultado = ordenar_burbuja(copia)
        sucursales = [fila[0] for fila in resultado]
        assert sucursales == sorted(sucursales), "El orden de sucursales no debe cambiar"

    def test_lista_vacia(self):
        """Ordenar una lista vacía debe retornar lista vacía sin errores."""
        resultado = ordenar_burbuja([])
        assert resultado == []


# ---------------------------------------------------------------------------
# Tests: calcular_importe
# ---------------------------------------------------------------------------

class TestCalcularImporte:

    def test_calculo_basico(self):
        """10 unidades a $5.50 deben dar $55.00."""
        assert calcular_importe('10', '5.50') == pytest.approx(55.0)

    def test_calculo_con_cantidad_cero(self):
        """Cantidad 0 siempre da importe 0 sin importar el precio."""
        assert calcular_importe('0', '100.00') == pytest.approx(0.0)

    def test_calculo_precio_decimal(self):
        """El cálculo debe manejar precios con decimales correctamente."""
        assert calcular_importe('3', '1.33') == pytest.approx(3.99)


# ---------------------------------------------------------------------------
# Tests: procesar_datos
# ---------------------------------------------------------------------------

class TestProcesarDatos:

    def test_total_sucursales(self):
        """Debe contar correctamente el número de sucursales únicas."""
        resultado = procesar_datos(FILAS_ORDENADAS)
        assert resultado['total_sucursales'] == 2

    def test_total_importe_general(self):
        """El importe total de todas las sucursales debe ser $323.50."""
        resultado = procesar_datos(FILAS_ORDENADAS)
        assert resultado['total_importe'] == pytest.approx(323.50, rel=1e-3)

    def test_mayor_producto_sucursal_1(self):
        """En S01, P001 debe ser el de mayor importe ($85.00)."""
        resultado = procesar_datos(FILAS_ORDENADAS)
        suc1 = resultado['sucursales'][0]
        assert suc1['mayor_producto'] == 'P001'
        assert suc1['mayor_importe'] == pytest.approx(85.0)

    def test_menor_producto_sucursal_1(self):
        """En S01, P002 debe ser el de menor importe ($60.00)."""
        resultado = procesar_datos(FILAS_ORDENADAS)
        suc1 = resultado['sucursales'][0]
        assert suc1['menor_producto'] == 'P002'
        assert suc1['menor_importe'] == pytest.approx(60.0)

    def test_mayor_producto_sucursal_2(self):
        """En S02, P003 debe ser el de mayor importe ($96.00)."""
        resultado = procesar_datos(FILAS_ORDENADAS)
        suc2 = resultado['sucursales'][1]
        assert suc2['mayor_producto'] == 'P003'
        assert suc2['mayor_importe'] == pytest.approx(96.0)

    def test_datos_vacios_retorna_ceros(self):
        """Con lista vacía debe retornar 0 sucursales y $0 de importe."""
        resultado = procesar_datos([])
        assert resultado['total_sucursales'] == 0
        assert resultado['total_importe'] == pytest.approx(0.0)
        assert resultado['sucursales'] == []

    def test_estructura_retorno(self):
        """El resultado debe contener las claves esperadas."""
        resultado = procesar_datos(FILAS_ORDENADAS)
        assert 'sucursales' in resultado
        assert 'total_sucursales' in resultado
        assert 'total_importe' in resultado
