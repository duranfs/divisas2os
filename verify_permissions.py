# -*- coding: utf-8 -*-
# Script para verificar permisos de usuario
# Ejecutar desde web2py shell: python web2py.py -S divisas2os -M -R verify_permissions.py

print("=== VERIFICACION DE PERMISOS ===")

if auth.user:
    print(f"Usuario actual: {auth.user.first_name} {auth.user.last_name}")
    print(f"Email: {auth.user.email}")
    print(f"ID: {auth.user.id}")
    
    # Verificar membresias
    if hasattr(auth, 'user_groups') and auth.user_groups:
        print("Grupos del usuario:")
        for group_id, group in auth.user_groups.items():
            if hasattr(group, 'role'):
                print(f"  - {group.role}")
            else:
                print(f"  - {group}")
    
    # Verificar permisos especificos
    es_admin = auth.has_membership('administrador')
    es_operador = auth.has_membership('operador')
    es_cliente = auth.has_membership('cliente')
    
    print(f"Es administrador: {es_admin}")
    print(f"Es operador: {es_operador}")
    print(f"Es cliente: {es_cliente}")
    
    puede_registrar = es_admin or es_operador
    print(f"Puede registrar clientes: {puede_registrar}")
    
    if not puede_registrar:
        print("PROBLEMA: El usuario no tiene permisos para registrar clientes")
        print("   Solucion: Asignar rol de 'administrador' u 'operador'")
else:
    print("No hay usuario logueado")
    print("   Solucion: Iniciar sesion primero")