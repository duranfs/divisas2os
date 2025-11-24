# -*- coding: utf-8 -*-
"""
Script para limpiar TODO el sistema y empezar desde cero
ADVERTENCIA: Esto eliminará:
- Todas las transacciones de divisas
- Todos los saldos de cuentas (los pondrá en 0)
- Todas las remesas y límites
- Todos los movimientos de remesas
- Todo el historial de operaciones
"""

import sys
import os

# Configurar path para web2py
web2py_path = r'C:\web2py'
sys.path.insert(0, web2py_path)

os.chdir(web2py_path)

# Importar web2py
from gluon import *
from gluon.shell import env

# Cargar el entorno de la aplicación
myenv = env('divisas2os', import_models=True)
db = myenv['db']

print("=" * 70)
print("LIMPIEZA COMPLETA DEL SISTEMA")
print("=" * 70)

# Contar registros antes
count_transacciones = db(db.transacciones.id > 0).count()
count_cuentas = db(db.cuentas.id > 0).count()
count_remesas = db(db.remesas_diarias.id > 0).count() if hasattr(db, 'remesas_diarias') else 0
count_limites = db(db.limites_venta.id > 0).count() if hasattr(db, 'limites_venta') else 0
count_movimientos = db(db.movimientos_remesas.id > 0).count() if hasattr(db, 'movimientos_remesas') else 0

print(f"\n📊 REGISTROS ACTUALES:")
print(f"   Transacciones: {count_transacciones}")
print(f"   Cuentas con saldo: {count_cuentas}")
if hasattr(db, 'remesas_diarias'):
    print(f"   Remesas Diarias: {count_remesas}")
    print(f"   Límites de Venta: {count_limites}")
    print(f"   Movimientos de Remesas: {count_movimientos}")

print("\n⚠️  ADVERTENCIA: Esto eliminará/reseteará:")
print("   1. ❌ Todas las transacciones de divisas")
print("   2. 🔄 Todos los saldos de cuentas (se pondrán en 0)")
if hasattr(db, 'remesas_diarias'):
    print("   3. ❌ Todas las remesas diarias")
    print("   4. ❌ Todos los límites de venta")
    print("   5. ❌ Todos los movimientos de remesas")
print("\n   ⚠️  LAS CUENTAS Y CLIENTES NO SE ELIMINARÁN, solo se resetearán los saldos")

respuesta = input("\n¿Continuar? (SI/NO): ").strip().upper()

if respuesta != 'SI':
    print("\n❌ Operación cancelada.")
    sys.exit(0)

print("\n🗑️  Eliminando/Reseteando registros...")

try:
    # 1. Eliminar transacciones
    deleted_transacciones = db(db.transacciones.id > 0).delete()
    print(f"   ✓ Transacciones eliminadas: {deleted_transacciones}")
    
    # 2. Resetear saldos de todas las cuentas a 0
    count_cuentas_reset = db(db.cuentas.id > 0).update(
        saldo_ves=0,
        saldo_usd=0,
        saldo_eur=0,
        saldo_usdt=0
    )
    print(f"   ✓ Saldos de cuentas reseteados: {count_cuentas_reset}")
    
    # 3. Eliminar movimientos de remesas (si existe la tabla)
    if hasattr(db, 'movimientos_remesas'):
        deleted_movimientos = db(db.movimientos_remesas.id > 0).delete()
        print(f"   ✓ Movimientos de remesas eliminados: {deleted_movimientos}")
    
    # 4. Eliminar límites de venta (si existe la tabla)
    if hasattr(db, 'limites_venta'):
        deleted_limites = db(db.limites_venta.id > 0).delete()
        print(f"   ✓ Límites de venta eliminados: {deleted_limites}")
    
    # 5. Eliminar remesas diarias (si existe la tabla)
    if hasattr(db, 'remesas_diarias'):
        deleted_remesas = db(db.remesas_diarias.id > 0).delete()
        print(f"   ✓ Remesas diarias eliminadas: {deleted_remesas}")
    
    # Commit de los cambios
    db.commit()
    
    print("\n✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
    print("\n📊 REGISTROS DESPUÉS DE LA LIMPIEZA:")
    print(f"   Transacciones: {db(db.transacciones.id > 0).count()}")
    print(f"   Cuentas: {db(db.cuentas.id > 0).count()} (saldos en 0)")
    if hasattr(db, 'remesas_diarias'):
        print(f"   Remesas Diarias: {db(db.remesas_diarias.id > 0).count()}")
        print(f"   Límites de Venta: {db(db.limites_venta.id > 0).count()}")
        print(f"   Movimientos de Remesas: {db(db.movimientos_remesas.id > 0).count()}")
    
    print("\n🎉 Sistema limpio. Puedes empezar desde cero.")
    print("   ℹ️  Los clientes y cuentas siguen existiendo, solo con saldos en 0.")
    
except Exception as e:
    print(f"\n❌ ERROR durante la limpieza: {str(e)}")
    db.rollback()
    print("   Se hizo rollback de los cambios.")
    sys.exit(1)

print("\n" + "=" * 70)
