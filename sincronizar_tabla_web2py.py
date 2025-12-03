# -*- coding: utf-8 -*-
"""
Script para sincronizar los archivos .table de web2py con la estructura real de la BD
Esto resuelve el error "duplicate column name: moneda"
"""

import os
import sqlite3

print("\n" + "=" * 80)
print("SINCRONIZACIÓN DE ARCHIVOS .TABLE DE WEB2PY")
print("=" * 80)

# Rutas
db_path = r'C:\web2py\applications\divisas2os\databases\storage.sqlite'
databases_dir = r'C:\web2py\applications\divisas2os\databases'

# Conectar a la BD
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Obtener estructura real de la tabla cuentas
cursor.execute("PRAGMA table_info(cuentas)")
columnas_reales = cursor.fetchall()

print("\nEstructura REAL de la tabla 'cuentas' en la BD:")
print("-" * 80)
for col in columnas_reales:
    print(f"  {col[1]} ({col[2]})")

# Buscar archivo .table de cuentas
print("\n" + "=" * 80)
print("Buscando archivos .table...")
print("=" * 80)

table_files = [f for f in os.listdir(databases_dir) if f.endswith('.table')]
cuentas_table_file = None

for table_file in table_files:
    with open(os.path.join(databases_dir, table_file), 'r', encoding='utf-8') as f:
        content = f.read()
        if "'cuentas'" in content or '"cuentas"' in content:
            cuentas_table_file = table_file
            break

if cuentas_table_file:
    print(f"\n✅ Encontrado archivo .table: {cuentas_table_file}")
    
    # Hacer backup del archivo .table
    table_path = os.path.join(databases_dir, cuentas_table_file)
    backup_path = table_path + '.backup'
    
    import shutil
    shutil.copy2(table_path, backup_path)
    print(f"✅ Backup creado: {backup_path}")
    
    # Leer contenido actual
    with open(table_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\nContenido actual del archivo .table:")
    print("-" * 80)
    print(content[:500] + "..." if len(content) > 500 else content)
    
    print("\n" + "=" * 80)
    print("SOLUCIÓN")
    print("=" * 80)
    print("\nPara resolver el error 'duplicate column name', se recomienda:")
    print("\n1. OPCIÓN RÁPIDA (Recomendada):")
    print("   - Eliminar todos los archivos .table")
    print("   - web2py los regenerará automáticamente")
    print(f"\n   Comando: del {databases_dir}\\*.table")
    
    print("\n2. OPCIÓN MANUAL:")
    print("   - Editar el archivo .table manualmente")
    print("   - Asegurar que incluya los campos 'moneda' y 'saldo'")
    
    respuesta = input("\n¿Desea eliminar los archivos .table ahora? (SI/NO): ")
    
    if respuesta.strip().upper() == 'SI':
        print("\nEliminando archivos .table...")
        for table_file in table_files:
            try:
                os.remove(os.path.join(databases_dir, table_file))
                print(f"  ✅ Eliminado: {table_file}")
            except Exception as e:
                print(f"  ❌ Error al eliminar {table_file}: {str(e)}")
        
        print("\n✅ Archivos .table eliminados")
        print("\nweb2py los regenerará automáticamente en el próximo inicio")
    else:
        print("\n⚠️  No se eliminaron los archivos .table")
        print("   Deberá hacerlo manualmente o editar el archivo")
else:
    print("\n⚠️  No se encontró archivo .table para la tabla 'cuentas'")
    print("   Esto es normal si es la primera vez que se ejecuta")

conn.close()

print("\n" + "=" * 80)
print("FINALIZADO")
print("=" * 80)
