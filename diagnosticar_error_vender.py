#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnostico del error en vender
"""

print("="*80)
print("DIAGNOSTICO ERROR EN VENDER")
print("="*80)

try:
    # Test 1: Verificar que obtener_tasas_actuales funciona
    print("\n[TEST 1] Verificar obtener_tasas_actuales()")
    tasas = obtener_tasas_actuales()
    if tasas:
        print(f"  Tipo: {type(tasas)}")
        print(f"  USD/VES: {tasas.usd_ves if hasattr(tasas, 'usd_ves') else 'NO EXISTE'}")
        print(f"  EUR/VES: {tasas.eur_ves if hasattr(tasas, 'eur_ves') else 'NO EXISTE'}")
        print(f"  Fecha: {tasas.fecha if hasattr(tasas, 'fecha') else 'NO EXISTE'}")
        print("  OK - obtener_tasas_actuales funciona")
    else:
        print("  ERROR - No hay tasas")
except Exception as e:
    print(f"  ERROR: {str(e)}")

try:
    # Test 2: Verificar generar_numero_cuenta_por_moneda
    print("\n[TEST 2] Verificar generar_numero_cuenta_por_moneda()")
    numero = generar_numero_cuenta_por_moneda('VES')
    print(f"  Numero generado: {numero}")
    print("  OK - generar_numero_cuenta_por_moneda funciona")
except Exception as e:
    print(f"  ERROR: {str(e)}")

try:
    # Test 3: Verificar generar_comprobante_unico
    print("\n[TEST 3] Verificar generar_comprobante_unico()")
    comprobante = generar_comprobante_unico('VENT')
    print(f"  Comprobante: {comprobante}")
    print("  OK - generar_comprobante_unico funciona")
except Exception as e:
    print(f"  ERROR: {str(e)}")

try:
    # Test 4: Verificar calcular_comision
    print("\n[TEST 4] Verificar calcular_comision()")
    from decimal import Decimal
    comision = calcular_comision(Decimal('1000'), 'venta')
    print(f"  Comision: {comision}")
    print("  OK - calcular_comision funciona")
except Exception as e:
    print(f"  ERROR: {str(e)}")

try:
    # Test 5: Verificar estructura de cuentas
    print("\n[TEST 5] Verificar estructura de cuentas")
    cuenta = db(db.cuentas).select(limitby=(0,1)).first()
    if cuenta:
        print(f"  Tiene moneda: {hasattr(cuenta, 'moneda')}")
        print(f"  Tiene saldo: {hasattr(cuenta, 'saldo')}")
        print(f"  Moneda: {cuenta.moneda if hasattr(cuenta, 'moneda') else 'NO EXISTE'}")
        print(f"  Saldo: {cuenta.saldo if hasattr(cuenta, 'saldo') else 'NO EXISTE'}")
        print("  OK - Estructura de cuentas correcta")
except Exception as e:
    print(f"  ERROR: {str(e)}")

try:
    # Test 6: Verificar estructura de transacciones
    print("\n[TEST 6] Verificar estructura de transacciones")
    print("  Campos esperados:")
    print(f"    cuenta_id: {hasattr(db.transacciones, 'cuenta_id')}")
    print(f"    tasa_aplicada: {hasattr(db.transacciones, 'tasa_aplicada')}")
    print(f"    numero_comprobante: {hasattr(db.transacciones, 'numero_comprobante')}")
    print("  OK - Estructura de transacciones verificada")
except Exception as e:
    print(f"  ERROR: {str(e)}")

print("\n"+"="*80)
print("DIAGNOSTICO COMPLETADO")
print("="*80)
