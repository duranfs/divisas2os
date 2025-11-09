#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar el formulario de registro mediante web2py
"""

import os
import sys

def test_registro_web2py():
    """
    Prueba el registro de cliente usando web2py
    """
    print("=== PRUEBA DEL REGISTRO DE CLIENTE ===")
    
    # Cambiar al directorio de web2py
    web2py_path = os.path.dirname(os.path.dirname(os.getcwd()))
    print(f"Directorio web2py: {web2py_path}")
    
    # Datos de prueba
    test_data = {
        'first_name': 'María Elena',
        'last_name': 'González Rodríguez',
        'cedula': 'V-87654321',
        'email': 'maria.gonzalez.test@email.com',
        'telefono': '04241234567',
        'direccion': 'Calle 123, Maracaibo, Zulia',
        'fecha_nacimiento': '1985-03-20',
        'password': 'password123',
        'password_confirm': 'password123'
    }
    
    print("\n1. Datos de prueba:")
    for key, value in test_data.items():
        if 'password' not in key:
            print(f"   {key}: {value}")
        else:
            print(f"   {key}: {'*' * len(value)}")
    
    print("\n2. Verificando que no existe el email en la BD...")
    
    # Crear script SQL para verificar
    sql_check = f"""
    SELECT COUNT(*) as count FROM auth_user WHERE email = '{test_data['email']}';
    SELECT COUNT(*) as count FROM clientes WHERE cedula = '{test_data['cedula']}';
    """
    
    with open('check_existing_user.sql', 'w') as f:
        f.write(sql_check)
    
    print("   📝 Script SQL creado: check_existing_user.sql")
    
    print("\n3. Creando script de prueba de registro...")
    
    # Crear script de prueba que simule el POST
    test_script = f'''
import sys
import os
sys.path.insert(0, '{web2py_path}')

from gluon import *
from gluon.storage import Storage

# Simular request con datos de prueba
request = Storage()
request.vars = Storage()
request.vars.first_name = "{test_data['first_name']}"
request.vars.last_name = "{test_data['last_name']}"
request.vars.cedula = "{test_data['cedula']}"
request.vars.email = "{test_data['email']}"
request.vars.telefono = "{test_data['telefono']}"
request.vars.direccion = "{test_data['direccion']}"
request.vars.fecha_nacimiento = "{test_data['fecha_nacimiento']}"
request.vars.password = "{test_data['password']}"
request.vars.password_confirm = "{test_data['password_confirm']}"

print("Datos de request.vars configurados")
print("Email:", request.vars.email)
print("Cédula:", request.vars.cedula)

# Simular response y session
response = Storage()
response.flash = ""
session = Storage()

print("\\nSimulando registro de cliente...")
print("Nota: Este script requiere ejecutarse desde web2py para funcionar completamente")
'''
    
    with open('test_registro_simulation.py', 'w') as f:
        f.write(test_script)
    
    print("   📝 Script de simulación creado: test_registro_simulation.py")
    
    print("\n4. Verificando estructura de archivos necesarios...")
    
    archivos_necesarios = [
        'controllers/clientes.py',
        'views/clientes/registrar.html',
        'models/db.py',
        'databases/storage.sqlite'
    ]
    
    archivos_ok = 0
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            archivos_ok += 1
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo}")
    
    print(f"\n   📊 Archivos encontrados: {archivos_ok}/{len(archivos_necesarios)}")
    
    print("\n5. Creando script de verificación de permisos...")
    
    # Script para verificar permisos del usuario actual
    permisos_script = '''
# Script para verificar permisos de usuario
# Ejecutar desde web2py shell: python web2py.py -S divisas2os -M -R verify_permissions.py

print("=== VERIFICACIÓN DE PERMISOS ===")

if auth.user:
    print(f"Usuario actual: {auth.user.first_name} {auth.user.last_name}")
    print(f"Email: {auth.user.email}")
    print(f"ID: {auth.user.id}")
    
    # Verificar membresías
    if hasattr(auth, 'user_groups') and auth.user_groups:
        print("Grupos del usuario:")
        for group_id, group in auth.user_groups.items():
            if hasattr(group, 'role'):
                print(f"  - {group.role}")
            else:
                print(f"  - {group}")
    
    # Verificar permisos específicos
    es_admin = auth.has_membership('administrador')
    es_operador = auth.has_membership('operador')
    es_cliente = auth.has_membership('cliente')
    
    print(f"Es administrador: {es_admin}")
    print(f"Es operador: {es_operador}")
    print(f"Es cliente: {es_cliente}")
    
    puede_registrar = es_admin or es_operador
    print(f"Puede registrar clientes: {puede_registrar}")
    
    if not puede_registrar:
        print("⚠️  PROBLEMA: El usuario no tiene permisos para registrar clientes")
        print("   Solución: Asignar rol de 'administrador' u 'operador'")
else:
    print("❌ No hay usuario logueado")
    print("   Solución: Iniciar sesión primero")
'''
    
    with open('verify_permissions.py', 'w') as f:
        f.write(permisos_script)
    
    print("   📝 Script de verificación creado: verify_permissions.py")
    
    print("\n6. Instrucciones para probar el formulario:")
    print("   1. Iniciar web2py:")
    print("      python web2py.py -a <password> -i 127.0.0.1 -p 8000")
    print("   2. Ir a: http://127.0.0.1:8000/divisas2os/default/user/login")
    print("   3. Iniciar sesión como administrador")
    print("   4. Verificar permisos:")
    print("      python web2py.py -S divisas2os -M -R verify_permissions.py")
    print("   5. Ir a: http://127.0.0.1:8000/divisas2os/clientes/registrar")
    print("   6. Llenar el formulario con los datos de prueba")
    
    print("\n7. Si el formulario no funciona, verificar:")
    print("   - Logs de web2py en la consola")
    print("   - Consola del navegador (F12) para errores JavaScript")
    print("   - Permisos del usuario (debe ser admin/operador)")
    print("   - Estado de la base de datos")
    
    return archivos_ok == len(archivos_necesarios)

if __name__ == "__main__":
    resultado = test_registro_web2py()
    print(f"\n{'='*60}")
    if resultado:
        print("✅ PREPARACIÓN COMPLETA - Listo para probar el formulario")
    else:
        print("❌ FALTAN ARCHIVOS - Verificar estructura del proyecto")
    print(f"{'='*60}")