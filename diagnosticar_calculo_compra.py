# -*- coding: utf-8 -*-
"""
Script para diagnosticar el cálculo de compra de divisas
"""

import sys
import os

# Agregar el directorio de web2py al path
web2py_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, web2py_path)

from decimal import Decimal, ROUND_HALF_UP

# Simular el cálculo que hace el sistema
def simular_compra(cantidad_divisa_deseada, tasa_compra, tasa_aplicada):
    """
    Simula el cálculo de compra tal como lo hace el sistema
    """
    print(f"\n{'='*60}")
    print(f"SIMULACIÓN DE COMPRA")
    print(f"{'='*60}")
    print(f"Cantidad de USD deseada: {cantidad_divisa_deseada}")
    print(f"Tasa de compra (para calcular VES): {tasa_compra}")
    print(f"Tasa aplicada (para calcular USD final): {tasa_aplicada}")
    print(f"{'-'*60}")
    
    # Paso 1: Calcular VES necesarios (línea 240)
    cantidad_divisa = Decimal(str(cantidad_divisa_deseada))
    tasa_compra_dec = Decimal(str(tasa_compra))
    monto_origen = cantidad_divisa * tasa_compra_dec
    
    print(f"\nPASO 1: Calcular VES necesarios")
    print(f"  monto_origen = {cantidad_divisa} * {tasa_compra_dec}")
    print(f"  monto_origen = {monto_origen} VES")
    
    # Paso 2: Calcular USD que recibirá (línea 313)
    tasa_aplicada_dec = Decimal(str(tasa_aplicada))
    monto_destino = monto_origen / tasa_aplicada_dec
    monto_destino = monto_destino.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    print(f"\nPASO 2: Calcular USD que recibirá")
    print(f"  monto_destino = {monto_origen} / {tasa_aplicada_dec}")
    print(f"  monto_destino = {monto_destino} USD (redondeado)")
    
    print(f"\n{'='*60}")
    print(f"RESULTADO:")
    print(f"  Quería comprar: {cantidad_divisa_deseada} USD")
    print(f"  Pagó: {monto_origen} VES")
    print(f"  Recibió: {monto_destino} USD")
    print(f"  Diferencia: {monto_destino - cantidad_divisa} USD")
    print(f"{'='*60}\n")
    
    return {
        'monto_origen': monto_origen,
        'monto_destino': monto_destino,
        'diferencia': monto_destino - cantidad_divisa
    }

# Caso 1: Tasas iguales (correcto)
print("\n" + "="*60)
print("CASO 1: Tasas iguales (comportamiento esperado)")
print("="*60)
simular_compra(50, 36.50, 36.50)

# Caso 2: Tasas diferentes (problema actual)
print("\n" + "="*60)
print("CASO 2: Tasas diferentes (posible problema)")
print("="*60)
simular_compra(50, 36.50, 36.20)

# Caso 3: Diferencia mayor
print("\n" + "="*60)
print("CASO 3: Diferencia mayor entre tasas")
print("="*60)
simular_compra(50, 37.00, 36.50)

print("\n" + "="*60)
print("CONCLUSIÓN:")
print("="*60)
print("Si las tasas son diferentes, el usuario recibirá más o menos")
print("divisas de las que solicitó. El sistema debería usar UNA sola")
print("tasa consistente en todo el cálculo.")
print("="*60)
