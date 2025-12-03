# -*- coding: utf-8 -*-
"""
Script para preparar la base de datos para la migración
Agrega columnas 'moneda' y 'saldo' a la tabla cuentas
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
print("PREPARACIÓN DE BASE DE DATOS PARA MIGRACIÓN")
print("=" * 70)

try:
    print("\n1. Verificando estructura actual de la tabla 'cuentas'...")
    
    # Obtener columnas actuales
    columnas_actuales = db.executesql("PRAGMA table_info(cuentas)")
    columnas_nombres = [col[1] for col in columnas_actuales]
    
    print(f"   Columnas actuales: {', '.join(columnas_nombres)}")
    
    # Verificar si ya existen las columnas nuevas
    tiene_moneda = 'moneda' in columnas_nombres
    tiene_saldo = 'saldo' in columnas_nombres
    
    if tiene_moneda and tiene_saldo:
        print("   ✓ Las columnas 'moneda' y 'saldo' ya existen")
    else:
        print("\n2. Agregando columnas nuevas...")
        
        # Agregar columna 'moneda' si no existe
        if not tiene_moneda:
            print("   Agregando columna 'moneda'...")
            db.executesql("ALTER TABLE cuentas ADD COLUMN moneda VARCHAR(10) DEFAULT 'VES'")
            print("   ✓ Columna 'moneda' agregada")
        
        # Agregar columna 'saldo' si no existe
        if not tiene_saldo:
            print("   Agregando columna 'saldo'...")
            db.executesql("ALTER TABLE cuentas ADD COLUMN saldo DECIMAL(15,4) DEFAULT 0")
            print("   ✓ Columna 'saldo' agregada")
        
        db.commit()
    
    print("\n3. Creando índices para optimización...")
    
    # Crear índice compuesto cliente_id + moneda
    try:
        db.executesql("CREATE INDEX IF NOT EXISTS idx_cliente_moneda ON cuentas(cliente_id, moneda)")
        print("   ✓ Índice idx_cliente_moneda creado")
    except Exception as e:
        print(f"   ℹ️  Índice ya existe o error: {str(e)}")
    
    # Crear índice para búsquedas por moneda
    try:
        db.executesql("CREATE INDEX IF NOT EXISTS idx_moneda ON cuentas(moneda)")
        print("   ✓ Índice idx_moneda creado")
    except Exception as e:
        print(f"   ℹ️  Índice ya existe o error: {str(e)}")
    
    # Crear índice para estado
    try:
        db.executesql("CREATE INDEX IF NOT EXISTS idx_estado ON cuentas(estado)")
        print("   ✓ Índice idx_estado creado")
    except Exception as e:
        print(f"   ℹ️  Índice ya existe o error: {str(e)}")
    
    db.commit()
    
    print("\n4. Verificando estructura final...")
    columnas_finales = db.executesql("PRAGMA table_info(cuentas)")
    print(f"   Total de columnas: {len(columnas_finales)}")
    
    for col in columnas_finales:
        col_id, nombre, tipo, notnull, default, pk = col
        print(f"   - {nombre}: {tipo} {'(PK)' if pk else ''}")
    
    print("\n5. Estadísticas de la tabla...")
    total_cuentas = db(db.cuentas.id > 0).count()
    print(f"   Total de cuentas: {total_cuentas}")
    
    # Contar cuentas con saldos
    cuentas_con_ves = db(db.cuentas.saldo_ves > 0).count()
    cuentas_con_usd = db(db.cuentas.saldo_usd > 0).count()
    cuentas_con_eur = db(db.cuentas.saldo_eur > 0).count()
    cuentas_con_usdt = db(db.cuentas.saldo_usdt > 0).count()
    
    print(f"   Cuentas con saldo VES > 0: {cuentas_con_ves}")
    print(f"   Cuentas con saldo USD > 0: {cuentas_con_usd}")
    print(f"   Cuentas con saldo EUR > 0: {cuentas_con_eur}")
    print(f"   Cuentas con saldo USDT > 0: {cuentas_con_usdt}")
    
    total_cuentas_a_crear = cuentas_con_ves + cuentas_con_usd + cuentas_con_eur + cuentas_con_usdt
    print(f"\n   📊 Estimación: Se crearán ~{total_cuentas_a_crear} cuentas en la migración")
    
    print("\n" + "=" * 70)
    print("✅ BASE DE DATOS PREPARADA PARA MIGRACIÓN")
    print("=" * 70)
    print("\nPróximo paso: Ejecutar script de migración")
    print("Comando: python migrar_cuentas.py")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
    sys.exit(1)
