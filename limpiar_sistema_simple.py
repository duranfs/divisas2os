# -*- coding: utf-8 -*-
"""
Script SIMPLE para limpiar el sistema
"""

import sys
import os

# Configurar path para web2py
web2py_path = r'C:\web2py'
sys.path.insert(0, web2py_path)
os.chdir(web2py_path)

from gluon import *
from gluon.shell import env

# Cargar el entorno
myenv = env('divisas2os', import_models=True)
db = myenv['db']

print("=" * 70)
print("LIMPIEZA SIMPLE DEL SISTEMA")
print("=" * 70)

try:
    # 1. Eliminar transacciones
    print("\n1. Eliminando transacciones...")
    db.executesql("DELETE FROM transacciones")
    print("   ✓ Transacciones eliminadas")
    
    # 2. Resetear saldos
    print("\n2. Reseteando saldos de cuentas...")
    db.executesql("UPDATE cuentas SET saldo_ves=0, saldo_usd=0, saldo_eur=0, saldo_usdt=0")
    print("   ✓ Saldos reseteados")
    
    # 3. Eliminar remesas (si existen)
    try:
        print("\n3. Eliminando remesas...")
        db.executesql("DELETE FROM movimientos_remesas")
        db.executesql("DELETE FROM limites_venta")
        db.executesql("DELETE FROM remesas_diarias")
        print("   ✓ Remesas eliminadas")
    except:
        print("   ℹ️  No hay tablas de remesas")
    
    # Commit
    db.commit()
    
    print("\n" + "=" * 70)
    print("✅ LIMPIEZA COMPLETADA")
    print("=" * 70)
    
    # Verificar
    print("\n📊 VERIFICACIÓN:")
    transacciones = db.executesql("SELECT COUNT(*) FROM transacciones")[0][0]
    cuentas = db.executesql("SELECT COUNT(*) FROM cuentas")[0][0]
    print(f"   Transacciones: {transacciones}")
    print(f"   Cuentas: {cuentas} (con saldos en 0)")
    
    print("\n🎉 Sistema limpio!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
    sys.exit(1)

print("\n" + "=" * 70)
