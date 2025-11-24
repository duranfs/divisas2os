# -*- coding: utf-8 -*-
"""
Script simple para limpiar el sistema usando SQL directo
"""

import sys
import os
import sqlite3

# Path a la base de datos
db_path = r'C:\web2py\applications\divisas2os\databases\storage.sqlite'

print("=" * 70)
print("LIMPIEZA DEL SISTEMA")
print("=" * 70)

# Conectar a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Contar registros antes
cursor.execute("SELECT COUNT(*) FROM transacciones")
count_transacciones = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM cuentas")
count_cuentas = cursor.fetchone()[0]

print(f"\n📊 REGISTROS ACTUALES:")
print(f"   Transacciones: {count_transacciones}")
print(f"   Cuentas: {count_cuentas}")

print("\n⚠️  ADVERTENCIA: Esto hará:")
print("   1. ❌ Eliminar todas las transacciones")
print("   2. 🔄 Resetear todos los saldos a 0")

respuesta = input("\n¿Continuar? (SI/NO): ").strip().upper()

if respuesta != 'SI':
    print("\n❌ Operación cancelada.")
    conn.close()
    sys.exit(0)

print("\n🗑️  Limpiando...")

try:
    # 1. Eliminar transacciones
    cursor.execute("DELETE FROM transacciones")
    print(f"   ✓ Transacciones eliminadas: {cursor.rowcount}")
    
    # 2. Resetear saldos
    cursor.execute("""
        UPDATE cuentas 
        SET saldo_ves = 0, 
            saldo_usd = 0, 
            saldo_eur = 0, 
            saldo_usdt = 0
    """)
    print(f"   ✓ Saldos reseteados: {cursor.rowcount}")
    
    # 3. Limpiar remesas si existen
    try:
        cursor.execute("DELETE FROM movimientos_remesas")
        print(f"   ✓ Movimientos de remesas eliminados: {cursor.rowcount}")
        
        cursor.execute("DELETE FROM limites_venta")
        print(f"   ✓ Límites eliminados: {cursor.rowcount}")
        
        cursor.execute("DELETE FROM remesas_diarias")
        print(f"   ✓ Remesas eliminadas: {cursor.rowcount}")
    except sqlite3.OperationalError:
        print("   ℹ️  Tablas de remesas no encontradas (normal si no existen)")
    
    # Commit
    conn.commit()
    
    # Verificar
    cursor.execute("SELECT COUNT(*) FROM transacciones")
    final_transacciones = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM cuentas")
    final_cuentas = cursor.fetchone()[0]
    
    print("\n✅ LIMPIEZA COMPLETADA")
    print(f"\n📊 RESULTADO:")
    print(f"   Transacciones: {final_transacciones}")
    print(f"   Cuentas: {final_cuentas} (saldos en 0)")
    print("\n🎉 Sistema limpio!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    conn.rollback()
finally:
    conn.close()

print("\n" + "=" * 70)
