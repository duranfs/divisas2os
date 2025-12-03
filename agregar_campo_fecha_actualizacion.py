# -*- coding: utf-8 -*-
"""
Script para agregar el campo fecha_actualizacion a la tabla cuentas
"""

import sqlite3
import os

print("\n" + "=" * 80)
print("AGREGAR CAMPO fecha_actualizacion")
print("=" * 80)

# Ruta a la base de datos
db_path = r'C:\web2py\applications\divisas2os\databases\storage.sqlite'

if not os.path.exists(db_path):
    print(f"\n❌ No se encontró la base de datos en: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verificar si el campo ya existe
    cursor.execute("PRAGMA table_info(cuentas)")
    columnas = cursor.fetchall()
    columnas_nombres = [col[1] for col in columnas]
    
    if 'fecha_actualizacion' in columnas_nombres:
        print("\n✅ El campo 'fecha_actualizacion' ya existe")
    else:
        print("\n🔄 Agregando campo 'fecha_actualizacion'...")
        cursor.execute("""
            ALTER TABLE cuentas
            ADD COLUMN fecha_actualizacion TIMESTAMP
        """)
        conn.commit()
        print("✅ Campo agregado exitosamente")
    
    # Verificar
    cursor.execute("PRAGMA table_info(cuentas)")
    columnas = cursor.fetchall()
    
    print("\nColumnas en la tabla 'cuentas':")
    for col in columnas:
        print(f"  - {col[1]} ({col[2]})")
    
    print("\n" + "=" * 80)
    print("✅ COMPLETADO")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    conn.rollback()
finally:
    conn.close()
