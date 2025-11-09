#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para diagnosticar problemas comunes en web2py
"""

import os
import sys
import sqlite3
from datetime import datetime

# Configurar path para el proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

def diagnose_database():
    """Diagnosticar problemas de base de datos"""
    print("🔍 DIAGNÓSTICO DE BASE DE DATOS")
    print("-" * 40)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # Verificar tablas principales
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['auth_user', 'auth_group', 'auth_membership', 'clientes', 'cuentas']
        
        print("📋 Tablas encontradas:")
        for table in required_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  ✅ {table}: {count} registros")
            else:
                print(f"  ❌ {table}: NO ENCONTRADA")
        
        # Verificar roles
        print("\n👥 Roles del sistema:")
        cursor.execute("SELECT role FROM auth_group")
        roles = [row[0] for row in cursor.fetchall()]
        for role in roles:
            print(f"  • {role}")
        
        # Verificar membresías
        print("\n🔐 Membresías de usuarios:")
        cursor.execute("""
            SELECT u.email, g.role 
            FROM auth_user u
            JOIN auth_membership m ON u.id = m.user_id
            JOIN auth_group g ON m.group_id = g.id
            ORDER BY u.email
        """)
        memberships = cursor.fetchall()
        for email, role in memberships:
            print(f"  • {email}: {role}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False

def diagnose_files():
    """Diagnosticar archivos del proyecto"""
    print("\n📁 DIAGNÓSTICO DE ARCHIVOS")
    print("-" * 40)
    
    critical_files = [
        'models/db.py',
        'controllers/clientes.py',
        'controllers/cuentas.py',
        'views/clientes/listar.html',
        'views/cuentas/listar_todas.html'
    ]
    
    for file_path in critical_files:
        full_path = os.path.join(project_dir, file_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"  ✅ {file_path}: {size} bytes")
        else:
            print(f"  ❌ {file_path}: NO ENCONTRADO")
    
    return True

def diagnose_permissions():
    """Diagnosticar permisos y configuración"""
    print("\n🔐 DIAGNÓSTICO DE PERMISOS")
    print("-" * 40)
    
    try:
        # Verificar permisos de escritura en databases
        db_dir = os.path.join(project_dir, 'databases')
        if os.path.exists(db_dir):
            if os.access(db_dir, os.W_OK):
                print("  ✅ Directorio databases: escritura OK")
            else:
                print("  ❌ Directorio databases: sin permisos de escritura")
        else:
            print("  ❌ Directorio databases: no existe")
        
        # Verificar archivo de base de datos
        db_file = os.path.join(project_dir, 'databases', 'storage.sqlite')
        if os.path.exists(db_file):
            if os.access(db_file, os.R_OK | os.W_OK):
                print("  ✅ storage.sqlite: lectura/escritura OK")
            else:
                print("  ❌ storage.sqlite: permisos insuficientes")
        else:
            print("  ❌ storage.sqlite: no existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando permisos: {e}")
        return False

def suggest_solutions():
    """Sugerir soluciones para problemas comunes"""
    print("\n💡 SOLUCIONES SUGERIDAS")
    print("-" * 40)
    
    print("Si tienes problemas con las vistas:")
    print("  1. Verifica que el servidor web2py esté ejecutándose")
    print("  2. Accede como administrador (usuario con rol 'administrador')")
    print("  3. Limpia el cache del navegador")
    print("  4. Revisa los logs de web2py para errores específicos")
    
    print("\nSi no ves datos:")
    print("  1. Ejecuta: python tests/create_test_data.py")
    print("  2. Verifica que tengas permisos de administrador")
    print("  3. Revisa que las consultas JOIN funcionen")
    
    print("\nSi hay errores de roles:")
    print("  1. Verifica que tu usuario tenga un rol asignado")
    print("  2. Ejecuta el script de creación de roles")
    print("  3. Reinicia la sesión de web2py")
    
    print("\nURLs para probar:")
    print("  • Clientes: http://127.0.0.1:8000/divisas2os/clientes/listar")
    print("  • Cuentas: http://127.0.0.1:8000/divisas2os/cuentas/listar_todas")
    print("  • Dashboard: http://127.0.0.1:8000/divisas2os/default/dashboard")

def main():
    """Función principal de diagnóstico"""
    print("🔧 DIAGNÓSTICO COMPLETO DEL SISTEMA")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directorio: {project_dir}")
    print()
    
    results = []
    
    # Ejecutar diagnósticos
    results.append(diagnose_database())
    results.append(diagnose_files())
    results.append(diagnose_permissions())
    
    # Mostrar resumen
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("✅ SISTEMA EN BUEN ESTADO")
        print("\n🎉 El sistema debería funcionar correctamente")
    else:
        print("⚠️  SE ENCONTRARON PROBLEMAS")
        print("\n🔧 Revisa las secciones marcadas con ❌")
    
    suggest_solutions()
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)