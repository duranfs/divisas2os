#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verificar error en función vender
"""

print("="*80)
print("VERIFICACION DE FUNCION VENDER")
print("="*80)

# Test 1: Verificar que obtener_tasas_actuales funciona
print("\n[1] Verificando obtener_tasas_actuales...")
try:
    tasas = obtener_tasas_actuales()
    if tasas:
        print(f"OK - Tasas obtenidas")
        print(f"  USD/VES: {tasas.usd_ves if hasattr(tasas, 'usd_ves') else 'N/A'}")
        print(f"  EUR/VES: {tasas.eur_ves if hasattr(tasas, 'eur_ves') else 'N/A'}")
        print(f"  USDT/VES: {tasas.usdt_ves if hasattr(tasas, 'usdt_ves') else 'N/A'}")
    else:
        print("ERROR - No se obtuvieron tasas")
except Exception as e:
    print(f"ERROR: {str(e)}")

# Test 2: Verificar que generar_numero_cuenta_por_moneda funciona
print("\n[2] Verificando generar_numero_cuenta_por_moneda...")
try:
    numero = generar_numero_cuenta_por_moneda('USD')
    print(f"OK - Numero generado: {numero}")
except Exception as e:
    print(f"ERROR: {str(e)}")

# Test 3: Verificar estructura de cuentas
print("\n[3] Verificando estructura de cuentas...")
try:
    cuenta = db(db.cuentas).select(limitby=(0,1)).first()
    if cuenta:
        print(f"OK - Cuenta encontrada")
        print(f"  Tiene moneda: {hasattr(cuenta, 'moneda')}")
        print(f"  Tiene saldo: {hasattr(cuenta, 'saldo')}")
        if hasattr(cuenta, 'moneda'):
            print(f"  Moneda: {cuenta.moneda}")
        if hasattr(cuenta, 'saldo'):
            print(f"  Saldo: {cuenta.saldo}")
except Exception as e:
    print(f"ERROR: {str(e)}")

# Test 4: Verificar que calcular_comision funciona
print("\n[4] Verificando calcular_comision...")
try:
    from decimal import Decimal
    comision = calcular_comision(Decimal('100'), 'venta')
    print(f"OK - Comision calculada: {comision}")
except Exception as e:
    print(f"ERROR: {str(e)}")

print("\n"+"="*80)
print("VERIFICACION COMPLETADA")
print("="*80)
