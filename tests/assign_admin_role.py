#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para asignar rol de administrador a un usuario
"""

import os
import sys
import sqlite3
from datetime import datetime

# Configurar path para el proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

def assign_admin_role(email):
    """Asignar rol de administrador a un usuario por email"""
    print(f"🔐 ASIGNANDO ROL DE ADMINISTRADOR A: {email}")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # Buscar usuario por email
        cursor.execute("SELECT id, first_name, last_name FROM auth_user WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ Usuario con email '{email}' no encontrado")
            return False
        
        user_id, first_name, last_name = user
        print(f"✅ Usuario encontrado: {first_name} {last_name} (ID: {user_id})")
        
        # Buscar grupo administrador
        cursor.execute("SELECT id FROM auth_group WHERE role = 'administrador'")
        admin_group = cursor.fetchone()
        
        if not admin_group:
            print("❌ Grupo 'administrador' no encontrado")
            return False
        
        admin_group_id = admin_group[0]
        print(f"✅ Grupo administrador encontrado (ID: {admin_group_id})")
        
        # Verificar si ya tiene el rol
        cursor.execute("""
            SELECT id FROM auth_membership 
            WHERE user_id = ? AND group_id = ?
        """, (user_id, admin_group_id))
        
        existing_membership = cursor.fetchone()
        
        if existing_membership:
            print("ℹ️  El usuario ya tiene rol de administrador")
            return True
        
        # Asignar rol de administrador
        cursor.execute("""
            INSERT INTO auth_membership (user_id, group_id)
            VALUES (?, ?)
        """, (user_id, admin_group_id))
        
        conn.commit()
        print("✅ Rol de administrador asignado exitosamente")
        
        # Verificar asignación
        cursor.execute("""
            SELECT g.role FROM auth_membership m
            JOIN auth_group g ON m.group_id = g.id
            WHERE m.user_id = ?
        """, (user_id,))
        
        roles = [row[0] for row in cursor.fetchall()]
        print(f"📋 Roles actuales del usuario: {', '.join(roles)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error asignando rol: {e}")
        return False

def list_users():
    """Listar todos los usuarios del sistema"""
    print("👥 USUARIOS DEL SISTEMA")
    print("-" * 40)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.id, u.email, u.first_name, u.last_name,
                   GROUP_CONCAT(g.role, ', ') as roles
            FROM auth_user u
            LEFT JOIN auth_membership m ON u.id = m.user_id
            LEFT JOIN auth_group g ON m.group_id = g.id
            GROUP BY u.id, u.email, u.first_name, u.last_name
            ORDER BY u.id
        """)
        
        users = cursor.fetchall()
        
        for user_id, email, first_name, last_name, roles in users:
            roles_str = roles if roles else "sin roles"
            print(f"  {user_id}. {first_name} {last_name}")
            print(f"     Email: {email}")
            print(f"     Roles: {roles_str}")
            print()
        
        conn.close()
        return users
        
    except Exception as e:
        print(f"❌ Error listando usuarios: {e}")
        return []

def main():
    """Función principal"""
    print("🔐 GESTIÓN DE ROLES DE ADMINISTRADOR")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Listar usuarios existentes
    users = list_users()
    
    if not users:
        print("❌ No se pudieron cargar los usuarios")
        return False
    
    # Preguntar qué usuario hacer administrador
    print("¿A qué usuario deseas asignar rol de administrador?")
    print("Opciones:")
    print("1. duranfs.2012@gmail.com (ya es admin)")
    print("2. beto.jesus@gmail.com")
    print("3. ricardo.duran@gmail.com")
    print("4. Otro email")
    
    # Para automatizar, asignar a beto.jesus@gmail.com
    target_email = "beto.jesus@gmail.com"
    print(f"\n🎯 Asignando automáticamente a: {target_email}")
    
    success = assign_admin_role(target_email)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ ROL ASIGNADO EXITOSAMENTE")
        print("=" * 60)
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Reinicia tu sesión en web2py (logout/login)")
        print("2. Accede a las URLs de administración:")
        print("   • http://127.0.0.1:8000/divisas2os/clientes/listar")
        print("   • http://127.0.0.1:8000/divisas2os/cuentas/listar_todas")
        print("3. Verifica que puedas ver todos los datos")
        return True
    else:
        print("\n❌ ERROR ASIGNANDO ROL")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)