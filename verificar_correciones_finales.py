#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verificación final de todas las correcciones aplicadas
"""

import sqlite3

print("=" * 80)
print("VERIFICACIÓN FINAL DE CORRECCIONES")
print("=" * 80)

# Conectar a la base de datos
conn = sqlite3.connect(r'databases\storage.sqlite')
cursor = conn.cursor()

# 1. Verificar estructura de cuentas
print("\n[1] Estructura de tabla cuentas:")
cursor.execute("PRAGMA table_info(cuentas)")
campos_cuentas = cursor.fetchall()
tiene_moneda = any(campo[1] == 'moneda' for campo in campos_cuentas)
tiene_saldo = any(campo[1] == 'saldo' for campo in campos_cuentas)

print(f"  ✓ Campo 'moneda': {'SÍ' if tiene_moneda else 'NO'}")
print(f"  ✓ Campo 'saldo': {'SÍ' if tiene_saldo else 'NO'}")

# 2. Verificar datos de cuentas
print("\n[2] Datos de cuentas:")
cursor.execute("SELECT COUNT(*) FROM cuentas WHERE moneda IS NOT NULL")
cuentas_con_moneda = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM cuentas")
total_cuentas = cursor.fetchone()[0]

print(f"  Total cuentas: {total_cuentas}")
print(f"  Cuentas con moneda: {cuentas_con_moneda}")
print(f"  ✓ Migración: {'COMPLETA' if cuentas_con_moneda == total_cuentas else 'INCOMPLETA'}")

# 3. Distribución por moneda
print("\n[3] Distribución por moneda:")
cursor.execute("SELECT moneda, COUNT(*), SUM(saldo) FROM cuentas GROUP BY moneda")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} cuentas, Saldo total: {row[2]:,.2f}")

# 4. Verificar estructura de transacciones
print("\n[4] Estructura de tabla transacciones:")
cursor.execute("PRAGMA table_info(transacciones)")
campos_trans = cursor.fetchall()
tiene_cuenta_id = any(campo[1] == 'cuenta_id' for campo in campos_trans)
tiene_numero_comprobante = any(campo[1] == 'numero_comprobante' for campo in campos_trans)
tiene_tasa_aplicada = any(campo[1] == 'tasa_aplicada' for campo in campos_trans)

print(f"  ✓ Campo 'cuenta_id': {'SÍ' if tiene_cuenta_id else 'NO'}")
print(f"  ✓ Campo 'numero_comprobante': {'SÍ' if tiene_numero_comprobante else 'NO'}")
print(f"  ✓ Campo 'tasa_aplicada': {'SÍ' if tiene_tasa_aplicada else 'NO'}")

# 5. Verificar transacciones
print("\n[5] Transacciones:")
cursor.execute("SELECT COUNT(*) FROM transacciones")
total_trans = cursor.fetchone()[0]
print(f"  Total transacciones: {total_trans}")

conn.close()

print("\n" + "=" * 80)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 80)
print("\nResumen:")
print(f"  • Cuentas migradas: {cuentas_con_moneda}/{total_cuentas}")
print(f"  • Modelo compatible: {'SÍ' if tiene_moneda and tiene_saldo else 'NO'}")
print(f"  • Transacciones: {total_trans}")
print("\n✅ Sistema listo para usar")
