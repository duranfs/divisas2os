# -*- coding: utf-8 -*-
"""
Script para hacer backup de la base de datos antes de la migración
"""

import sys
import os
import shutil
from datetime import datetime

# Configurar path para web2py
web2py_path = r'C:\web2py'
sys.path.insert(0, web2py_path)
os.chdir(web2py_path)

print("=" * 70)
print("BACKUP DE BASE DE DATOS - ANTES DE MIGRACIÓN")
print("=" * 70)
print(f"\nFecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "=" * 70)

try:
    # Rutas
    db_path = os.path.join(web2py_path, 'applications', 'divisas2os', 'databases', 'storage.sqlite')
    backup_dir = os.path.join(web2py_path, 'applications', 'divisas2os', 'backups')
    
    # Crear directorio de backups si no existe
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✓ Directorio de backups creado: {backup_dir}")
    
    # Nombre del backup con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'storage_antes_migracion_{timestamp}.sqlite'
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Verificar que existe la BD
    if not os.path.exists(db_path):
        print(f"\n❌ ERROR: No se encontró la base de datos en: {db_path}")
        sys.exit(1)
    
    # Obtener tamaño de la BD
    db_size = os.path.getsize(db_path)
    db_size_mb = db_size / (1024 * 1024)
    
    print(f"\n📊 Información de la base de datos:")
    print(f"   Ubicación: {db_path}")
    print(f"   Tamaño: {db_size_mb:.2f} MB")
    
    # Realizar backup
    print(f"\n🔄 Realizando backup...")
    shutil.copy2(db_path, backup_path)
    
    # Verificar backup
    if os.path.exists(backup_path):
        backup_size = os.path.getsize(backup_path)
        if backup_size == db_size:
            print(f"✅ Backup completado exitosamente!")
            print(f"\n📁 Backup guardado en:")
            print(f"   {backup_path}")
            print(f"   Tamaño: {backup_size / (1024 * 1024):.2f} MB")
        else:
            print(f"⚠️  Advertencia: El tamaño del backup no coincide")
            print(f"   Original: {db_size_mb:.2f} MB")
            print(f"   Backup: {backup_size / (1024 * 1024):.2f} MB")
    else:
        print(f"❌ ERROR: No se pudo crear el backup")
        sys.exit(1)
    
    # Listar backups existentes
    print(f"\n📋 Backups disponibles:")
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.sqlite')]
    backups.sort(reverse=True)
    
    for backup in backups[:5]:  # Mostrar últimos 5
        backup_full_path = os.path.join(backup_dir, backup)
        size = os.path.getsize(backup_full_path) / (1024 * 1024)
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_full_path))
        print(f"   - {backup} ({size:.2f} MB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "=" * 70)
    print("✅ BACKUP COMPLETADO - Listo para migración")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERROR durante el backup: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
