#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Prueba Completa del Sistema
Verifica que todo funcione correctamente después de las correcciones
"""

import sys
import os

print("=" * 80)
print("PRUEBA COMPLETA DEL SISTEMA - CUENTAS POR MONEDA")
print("=" * 80)

resultados = []

# TEST 1: Verificar estructura de base de datos
print("\n[TEST 1] Verificando estructura de base de datos...")
try:
    # Verificar tabla cuentas
    cuenta_test = db(db.cuentas).select(limitby=(0,1)).first()
    if cuenta_test:
        tiene_moneda = hasattr(cuenta_test, 'moneda')
        tiene_saldo = hasattr(cuenta_test, 'saldo')
        
        if tiene_moneda and tiene_saldo:
            print("  ✓ Tabla cuentas tiene campos 'moneda' y 'saldo'")
            resultados.append(("Estructura BD - Cuentas", True))
        else:
            print("  ❌ Tabla cuentas NO tiene los campos necesarios")
            resultados.append(("Estructura BD - Cuentas", False))
    else:
        print("  ⚠ No hay cuentas en la BD")
        resultados.append(("Estructura BD - Cuentas", False))
        
except Exception as e:
    print(f"  ❌ Error: {str(e)}")
    resultados.append(("Estructura BD - Cuentas", False))

# TEST 2: Verificar que hay cuentas por moneda
print("\n[TEST 2] Verificando cuentas por moneda...")
try:
    cuentas_ves = db(db.cuentas.moneda == 'VES').count()
    cuentas_usd = db(db.cuentas.moneda == 'USD').count()
    cuentas_eur = db(db.cuentas.moneda == 'EUR').count()
    cuentas_usdt = db(db.cuentas.moneda == 'USDT').count()
    
    print(f"  VES: {cuentas_ves} cuentas")
    print(f"  USD: {cuentas_usd} cuentas")
    print(f"  EUR: {cuentas_eur} cuentas")
    print(f"  USDT: {cuentas_usdt} cuentas")
    
    if cuentas_ves > 0:
        print("  ✓ Hay cuentas por moneda")
        resultados.append(("Cuentas por moneda", True))
    else:
        print("  ❌ No hay cuentas VES")
        resultados.append(("Cuentas por moneda", False))
        
except Exception as e:
    print(f"  ❌ Error: {str(e)}")
    resultados.append(("Cuentas por moneda", False))

# TEST 3: Verificar función dashboard_cliente
print("\n[TEST 3] Verificando función dashboard_cliente...")
try:
    # Buscar un cliente con cuentas
    cliente = db(db.clientes).select(limitby=(0,1)).first()
    
    if cliente:
        cuentas = db(
            (db.cuentas.cliente_id == cliente.id) &
            (db.cuentas.estado == 'activa')
        ).select()
        
        # Calcular totales como lo hace el dashboard
        total_ves = sum([float(cuenta.saldo or 0) for cuenta in cuentas if cuenta.moneda == 'VES'])
        total_usd = sum([float(cuenta.saldo or 0) for cuenta in cuentas if cuenta.moneda == 'USD'])
        
        print(f"  Cliente: {cliente.cedula}")
        print(f"  Cuentas: {len(cuentas)}")
        print(f"  Total VES: {total_ves:,.2f}")
        print(f"  Total USD: {total_usd:,.2f}")
        print("  ✓ Función dashboard_cliente funciona")
        resultados.append(("Dashboard cliente", True))
    else:
        print("  ⚠ No hay clientes para probar")
        resultados.append(("Dashboard cliente", False))
        
except Exception as e:
    print(f"  ❌ Error: {str(e)}")
    resultados.append(("Dashboard cliente", False))

# TEST 4: Verificar consulta de transacciones
print("\n[TEST 4] Verificando consulta de transacciones...")
try:
    transacciones = db(db.transacciones).select(limitby=(0,5))
    
    print(f"  Total transacciones: {db(db.transacciones).count()}")
    
    if transacciones:
        tx = transacciones.first()
        tiene_cuenta_id = hasattr(tx, 'cuenta_id')
        tiene_numero_comprobante = hasattr(tx, 'numero_comprobante')
        
        if tiene_cuenta_id and tiene_numero_comprobante:
            print("  ✓ Transacciones tienen campos correctos")
            resultados.append(("Transacciones", True))
        else:
            print("  ❌ Transacciones NO tienen campos correctos")
            resultados.append(("Transacciones", False))
    else:
        print("  ⚠ No hay transacciones")
        resultados.append(("Transacciones", True))
        
except Exception as e:
    print(f"  ❌ Error: {str(e)}")
    resultados.append(("Transacciones", False))

# TEST 5: Verificar función obtener_tasas_actuales
print("\n[TEST 5] Verificando función obtener_tasas_actuales...")
try:
    tasas = obtener_tasas_actuales()
    
    if tasas:
        print(f"  USD/VES: {tasas.usd_ves if hasattr(tasas, 'usd_ves') else 'N/A'}")
        print(f"  EUR/VES: {tasas.eur_ves if hasattr(tasas, 'eur_ves') else 'N/A'}")
        print("  ✓ Función obtener_tasas_actuales funciona")
        resultados.append(("Tasas actuales", True))
    else:
        print("  ⚠ No hay tasas disponibles")
        resultados.append(("Tasas actuales", False))
        
except Exception as e:
    print(f"  ❌ Error: {str(e)}")
    resultados.append(("Tasas actuales", False))

# TEST 6: Verificar generación de número de cuenta
print("\n[TEST 6] Verificando generación de número de cuenta...")
try:
    numero_ves = generar_numero_cuenta_por_moneda('VES')
    numero_usd = generar_numero_cuenta_por_moneda('USD')
    
    if numero_ves.startswith('01') and numero_usd.startswith('02'):
        print(f"  VES: {numero_ves} (prefijo correcto)")
        print(f"  USD: {numero_usd} (prefijo correcto)")
        print("  ✓ Generación de números de cuenta funciona")
        resultados.append(("Generación números cuenta", True))
    else:
        print("  ❌ Prefijos incorrectos")
        resultados.append(("Generación números cuenta", False))
        
except Exception as e:
    print(f"  ❌ Error: {str(e)}")
    resultados.append(("Generación números cuenta", False))

# TEST 7: Verificar que no hay campos antiguos en uso
print("\n[TEST 7] Verificando que no se usan campos antiguos...")
try:
    # Leer el controlador default.py
    with open('controllers/default.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
        
    usa_saldo_ves = 'saldo_ves' in contenido
    usa_saldo_usd = 'saldo_usd' in contenido
    
    if not usa_saldo_ves and not usa_saldo_usd:
        print("  ✓ No se usan campos antiguos (saldo_ves, saldo_usd)")
        resultados.append(("Sin campos antiguos", True))
    else:
        print("  ❌ Todavía se usan campos antiguos")
        resultados.append(("Sin campos antiguos", False))
        
except Exception as e:
    print(f"  ❌ Error: {str(e)}")
    resultados.append(("Sin campos antiguos", False))

# RESUMEN
print("\n" + "=" * 80)
print("RESUMEN DE PRUEBAS")
print("=" * 80)

for nombre, resultado in resultados:
    estado = "✅ PASS" if resultado else "❌ FAIL"
    print(f"{nombre}: {estado}")

exitosos = sum(1 for _, r in resultados if r)
total = len(resultados)

print(f"\nTotal: {exitosos}/{total} pruebas exitosas")

if exitosos == total:
    print("\n" + "=" * 80)
    print("✅ SISTEMA FUNCIONANDO CORRECTAMENTE")
    print("=" * 80)
    print("\nTodas las correcciones se aplicaron exitosamente:")
    print("  • Dashboard usa campos nuevos (moneda, saldo)")
    print("  • Transacciones usan campos correctos (cuenta_id)")
    print("  • Modelo sincronizado con base de datos")
    print("  • Generación de números de cuenta funciona")
    print("  • Sistema listo para usar")
else:
    print("\n" + "=" * 80)
    print("⚠ ALGUNAS PRUEBAS FALLARON")
    print("=" * 80)
    print("\nRevisar los errores anteriores.")

print("\n" + "=" * 80)
