# -*- coding: utf-8 -*-
"""
Script para verificar si la tabla movimientos_remesas existe en la base de datos
"""

import sys
import os
import sqlite3

# Ruta a la base de datos
db_path = os.path.join('databases', 'storage.sqlite')

print("=" * 70)
print("VERIFICACIÓN DE TABLA movimientos_remesas")
print("=" * 70)

try:
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar si la tabla existe
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='movimientos_remesas'
    """)
    
    tabla_existe = cursor.fetchone()
    
    if tabla_existe:
        print("\n✓ La tabla 'movimientos_remesas' EXISTE")
        
        # Obtener estructura de la tabla
        cursor.execute("PRAGMA table_info(movimientos_remesas)")
        columnas = cursor.fetchall()
        
        print("\nEstructura de la tabla:")
        for col in columnas:
            print(f"  - {col[1]} ({col[2]})")
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM movimientos_remesas")
        count = cursor.fetchone()[0]
        print(f"\nTotal de registros: {count}")
        
        if count > 0:
            # Mostrar algunos registros
            cursor.execute("SELECT * FROM movimientos_remesas LIMIT 3")
            registros = cursor.fetchall()
            print("\nPrimeros 3 registros:")
            for reg in registros:
                print(f"  ID: {reg[0]}")
        else:
            print("\n⚠ La tabla está VACÍA (no tiene registros)")
    else:
        print("\n✗ La tabla 'movimientos_remesas' NO EXISTE")
        print("\nTablas disponibles en la base de datos:")
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """)
        tablas = cursor.fetchall()
        for tabla in tablas:
            print(f"  - {tabla[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")

print("\n" + "=" * 70)
