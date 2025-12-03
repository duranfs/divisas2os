# -*- coding: utf-8 -*-
"""
Script para verificar el estado de la base de datos directamente con SQLite
"""

import sqlite3
import os
from decimal import Decimal

print("\n" + "=" * 80)
print("VERIFICACIÓN DIRECTA DE LA BASE DE DATOS")
print("=" * 80)

# Ruta a la base de datos
db_path = r'C:\web2py\applications\divisas2os\databases\storage.sqlite'

if not os.path.exists(db_path):
    print(f"\n❌ No se encontró la base de datos en: {db_path}")
    exit(1)

print(f"\n✅ Base de datos encontrada: {db_path}")
print(f"   Tamaño: {os.path.getsize(db_path) / (1024 * 1024):.2f} MB")

try:
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Verificar estructura de la tabla cuentas
    print("\n1. Estructura de la tabla 'cuentas':")
    print("-" * 80)
    
    cursor.execute("PRAGMA table_info(cuentas)")
    columnas = cursor.fetchall()
    
    print("\nColumnas en la tabla 'cuentas':")
    for col in columnas:
        print(f"   - {col[1]} ({col[2]})")
    
    # Verificar si existen los nuevos campos
    columnas_nombres = [col[1] for col in columnas]
    tiene_moneda = 'moneda' in columnas_nombres
    tiene_saldo = 'saldo' in columnas_nombres
    
    print(f"\n   Campo 'moneda': {'✅ Existe' if tiene_moneda else '❌ No existe'}")
    print(f"   Campo 'saldo': {'✅ Existe' if tiene_saldo else '❌ No existe'}")
    
    # 2. Contar cuentas totales
    cursor.execute("SELECT COUNT(*) FROM cuentas")
    total_cuentas = cursor.fetchone()[0]
    print(f"\n2. Total de cuentas: {total_cuentas}")
    
    # 3. Verificar cuentas por moneda (si el campo existe)
    if tiene_moneda:
        print("\n3. Cuentas por moneda:")
        print("-" * 80)
        
        cursor.execute("""
            SELECT moneda, COUNT(*) as cantidad
            FROM cuentas
            WHERE moneda IS NOT NULL AND moneda != ''
            GROUP BY moneda
            ORDER BY moneda
        """)
        
        cuentas_por_moneda = cursor.fetchall()
        
        if cuentas_por_moneda:
            for moneda, cantidad in cuentas_por_moneda:
                print(f"   {moneda}: {cantidad} cuentas")
        else:
            print("   No hay cuentas con moneda asignada")
        
        # Cuentas sin moneda
        cursor.execute("""
            SELECT COUNT(*) FROM cuentas
            WHERE moneda IS NULL OR moneda = ''
        """)
        sin_moneda = cursor.fetchone()[0]
        print(f"   Sin moneda: {sin_moneda} cuentas")
    
    # 4. Verificar saldos en campos antiguos
    print("\n4. Saldos en campos antiguos:")
    print("-" * 80)
    
    if 'saldo_ves' in columnas_nombres:
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE saldo_ves > 0")
        print(f"   Cuentas con saldo_ves > 0: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT SUM(saldo_ves) FROM cuentas")
        total_ves = cursor.fetchone()[0] or 0
        print(f"   Total saldo_ves: {total_ves:,.2f}")
    
    if 'saldo_usd' in columnas_nombres:
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE saldo_usd > 0")
        print(f"   Cuentas con saldo_usd > 0: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT SUM(saldo_usd) FROM cuentas")
        total_usd = cursor.fetchone()[0] or 0
        print(f"   Total saldo_usd: {total_usd:,.2f}")
    
    if 'saldo_eur' in columnas_nombres:
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE saldo_eur > 0")
        print(f"   Cuentas con saldo_eur > 0: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT SUM(saldo_eur) FROM cuentas")
        total_eur = cursor.fetchone()[0] or 0
        print(f"   Total saldo_eur: {total_eur:,.2f}")
    
    if 'saldo_usdt' in columnas_nombres:
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE saldo_usdt > 0")
        print(f"   Cuentas con saldo_usdt > 0: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT SUM(saldo_usdt) FROM cuentas")
        total_usdt = cursor.fetchone()[0] or 0
        print(f"   Total saldo_usdt: {total_usdt:,.2f}")
    
    # 5. Verificar saldos en nuevo campo
    if tiene_saldo:
        print("\n5. Saldos en nuevo campo 'saldo':")
        print("-" * 80)
        
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE saldo > 0")
        print(f"   Cuentas con saldo > 0: {cursor.fetchone()[0]}")
        
        if tiene_moneda:
            cursor.execute("""
                SELECT moneda, SUM(saldo) as total
                FROM cuentas
                WHERE moneda IS NOT NULL AND moneda != ''
                GROUP BY moneda
                ORDER BY moneda
            """)
            
            saldos_por_moneda = cursor.fetchall()
            
            if saldos_por_moneda:
                print("\n   Saldos totales por moneda:")
                for moneda, total in saldos_por_moneda:
                    print(f"      {moneda}: {total:,.4f}")
            else:
                print("   No hay saldos en el nuevo campo")
    
    # 6. Verificar clientes
    print("\n6. Información de clientes:")
    print("-" * 80)
    
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]
    print(f"   Total de clientes: {total_clientes}")
    
    # 7. Verificar transacciones
    print("\n7. Información de transacciones:")
    print("-" * 80)
    
    cursor.execute("SELECT COUNT(*) FROM transacciones")
    total_transacciones = cursor.fetchone()[0]
    print(f"   Total de transacciones: {total_transacciones}")
    
    # Verificar si existen los nuevos campos en transacciones
    cursor.execute("PRAGMA table_info(transacciones)")
    columnas_trans = cursor.fetchall()
    columnas_trans_nombres = [col[1] for col in columnas_trans]
    
    if 'cuenta_origen_id' in columnas_trans_nombres:
        cursor.execute("""
            SELECT COUNT(*) FROM transacciones
            WHERE cuenta_origen_id IS NOT NULL AND cuenta_destino_id IS NOT NULL
        """)
        trans_con_cuentas = cursor.fetchone()[0]
        print(f"   Transacciones con cuenta_origen_id y cuenta_destino_id: {trans_con_cuentas}")
    
    # 8. CONCLUSIÓN
    print("\n" + "=" * 80)
    print("CONCLUSIÓN")
    print("=" * 80)
    
    if tiene_moneda and tiene_saldo:
        # Verificar si hay cuentas migradas
        cursor.execute("""
            SELECT COUNT(*) FROM cuentas
            WHERE moneda IS NOT NULL AND moneda != ''
        """)
        cuentas_migradas = cursor.fetchone()[0]
        
        if cuentas_migradas > 0:
            print("\n✅ LA MIGRACIÓN YA HA SIDO EJECUTADA")
            print(f"   Se encontraron {cuentas_migradas} cuentas con moneda asignada")
            print("\n   El sistema ya está usando el nuevo modelo de cuentas por moneda.")
            print("\n   Estado: MIGRACIÓN COMPLETADA")
        else:
            print("\n⚠️  Los campos existen pero NO hay cuentas migradas")
            print("   Los campos 'moneda' y 'saldo' existen en la tabla")
            print("   pero no hay cuentas con moneda asignada.")
            print("\n   Estado: PREPARADO PARA MIGRACIÓN")
    else:
        print("\n⚠️  La migración NO ha sido ejecutada")
        print("   Faltan los campos 'moneda' y/o 'saldo' en la tabla")
        print("\n   Estado: REQUIERE PREPARACIÓN")
    
    print("\n" + "=" * 80)
    
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
