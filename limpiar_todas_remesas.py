# -*- coding: utf-8 -*-
"""
Script para limpiar TODAS las remesas y empezar desde cero
ADVERTENCIA: Esto eliminará todos los datos de remesas, límites y movimientos
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
print("LIMPIEZA COMPLETA DE REMESAS")
print("=" * 70)

# Contar registros antes
count_remesas = db(db.remesas_diarias.id > 0).count()
count_limites = db(db.limites_venta.id > 0).count()
count_movimientos = db(db.movimientos_remesas.id > 0).count()

print(f"\n📊 REGISTROS ACTUALES:")
print(f"   Remesas Diarias: {count_remesas}")
print(f"   Límites de Venta: {count_limites}")
print(f"   Movimientos de Remesas: {count_movimientos}")

if count_remesas == 0 and count_limites == 0 and count_movimientos == 0:
    print("\n✅ No hay registros para eliminar. Base de datos ya está limpia.")
    sys.exit(0)

print("\n⚠️  ADVERTENCIA: Esto eliminará TODOS los registros de:")
print("   1. Remesas Diarias")
print("   2. Límites de Venta")
print("   3. Movimientos de Remesas")

respuesta = input("\n¿Estás seguro? Escribe 'SI' para confirmar: ")

if respuesta.upper() != 'SI':
    print("\n❌ Operación cancelada.")
    sys.exit(0)

print("\n🗑️  Eliminando registros...")

try:
    # Eliminar en orden (primero los que tienen referencias)
    
    # 1. Eliminar movimientos de remesas
    deleted_movimientos = db(db.movimientos_remesas.id > 0).delete()
    print(f"   ✓ Movimientos eliminados: {deleted_movimientos}")
    
    # 2. Eliminar límites de venta
    deleted_limites = db(db.limites_venta.id > 0).delete()
    print(f"   ✓ Límites eliminados: {deleted_limites}")
    
    # 3. Eliminar remesas diarias
    deleted_remesas = db(db.remesas_diarias.id > 0).delete()
    print(f"   ✓ Remesas eliminadas: {deleted_remesas}")
    
    # Commit de los cambios
    db.commit()
    
    print("\n✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
    print("\n📊 REGISTROS DESPUÉS DE LA LIMPIEZA:")
    print(f"   Remesas Diarias: {db(db.remesas_diarias.id > 0).count()}")
    print(f"   Límites de Venta: {db(db.limites_venta.id > 0).count()}")
    print(f"   Movimientos de Remesas: {db(db.movimientos_remesas.id > 0).count()}")
    
    print("\n🎉 Ahora puedes empezar a registrar remesas desde cero.")
    
except Exception as e:
    print(f"\n❌ ERROR durante la limpieza: {str(e)}")
    db.rollback()
    print("   Se hizo rollback de los cambios.")
    sys.exit(1)

print("\n" + "=" * 70)
