#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Prueba Simple del Sistema
"""

print("="*80)
print("PRUEBA DEL SISTEMA")
print("="*80)

# TEST 1: Cuentas
print("\n[TEST 1] Cuentas por moneda")
try:
    ves = db(db.cuentas.moneda == 'VES').count()
    usd = db(db.cuentas.moneda == 'USD').count()
    print(f"VES: {ves}, USD: {usd}")
    print("OK - Cuentas por moneda")
except Exception as e:
    print(f"ERROR: {str(e)}")

# TEST 2: Dashboard
print("\n[TEST 2] Dashboard cliente")
try:
    cliente = db(db.clientes).select(limitby=(0,1)).first()
    if cliente:
        cuentas = db((db.cuentas.cliente_id == cliente.id) & (db.cuentas.estado == 'activa')).select()
        total_ves = sum([float(c.saldo or 0) for c in cuentas if c.moneda == 'VES'])
        print(f"Cliente: {cliente.cedula}, Cuentas: {len(cuentas)}, VES: {total_ves:.2f}")
        print("OK - Dashboard funciona")
except Exception as e:
    print(f"ERROR: {str(e)}")

# TEST 3: Transacciones
print("\n[TEST 3] Transacciones")
try:
    total = db(db.transacciones).count()
    print(f"Total transacciones: {total}")
    print("OK - Transacciones")
except Exception as e:
    print(f"ERROR: {str(e)}")

print("\n"+"="*80)
print("PRUEBAS COMPLETADAS")
print("="*80)
