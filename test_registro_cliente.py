#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar el formulario de registro de clientes
"""

import sys
import os

# Agregar el directorio de web2py al path
sys.path.append('.')

def test_registro_cliente():
    """
    Prueba el formulario de registro de clientes
    """
    print("=== PRUEBA DEL FORMULARIO DE REGISTRO DE CLIENTES ===")
    
    try:
        # Simular el entorno de web2py
        from gluon import current
        from gluon.storage import Storage
        
        # Datos de prueba para el formulario
        test_data = {
            'first_name': 'Juan Carlos',
            'last_name': 'Pérez González',
            'cedula': 'V-12345678',
            'email': 'juan.perez.test@email.com',
            'telefono': '04141234567',
            'direccion': 'Av. Principal, Caracas',
            'fecha_nacimiento': '1990-05-15',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        
        print("1. Datos de prueba preparados:")
        for key, value in test_data.items():
            if 'password' not in key:
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: {'*' * len(value)}")
        
        print("\n2. Verificando estructura de la vista registrar.html...")
        
        # Leer el archivo de vista
        with open('views/clientes/registrar.html', 'r', encoding='utf-8') as f:
            vista_content = f.read()
        
        # Verificar elementos clave del formulario
        elementos_requeridos = [
            'form method="post"',
            'name="first_name"',
            'name="last_name"',
            'name="cedula"',
            'name="email"',
            'name="telefono"',
            'name="direccion"',
            'name="fecha_nacimiento"',
            'name="password"',
            'name="password_confirm"',
            'type="submit"'
        ]
        
        elementos_encontrados = []
        elementos_faltantes = []
        
        for elemento in elementos_requeridos:
            if elemento in vista_content:
                elementos_encontrados.append(elemento)
            else:
                elementos_faltantes.append(elemento)
        
        print(f"   ✅ Elementos encontrados: {len(elementos_encontrados)}/{len(elementos_requeridos)}")
        
        if elementos_faltantes:
            print("   ❌ Elementos faltantes:")
            for elemento in elementos_faltantes:
                print(f"      - {elemento}")
        else:
            print("   ✅ Todos los elementos del formulario están presentes")
        
        print("\n3. Verificando controlador clientes.py...")
        
        # Verificar que existe la función registrar
        with open('controllers/clientes.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        if 'def registrar():' in controller_content:
            print("   ✅ Función registrar() encontrada en el controlador")
        else:
            print("   ❌ Función registrar() NO encontrada en el controlador")
        
        # Verificar elementos clave del controlador
        controller_checks = [
            'auth.requires_login()',
            'request.vars.first_name',
            'db.auth_user.insert',
            'db.clientes.insert',
            'generar_numero_cuenta()',
            'return dict(form=form'
        ]
        
        controller_ok = True
        for check in controller_checks:
            if check not in controller_content:
                print(f"   ❌ Falta: {check}")
                controller_ok = False
        
        if controller_ok:
            print("   ✅ Controlador parece estar completo")
        
        print("\n4. Verificando función generar_numero_cuenta()...")
        
        if 'def generar_numero_cuenta():' in controller_content:
            print("   ✅ Función generar_numero_cuenta() encontrada")
        else:
            print("   ❌ Función generar_numero_cuenta() NO encontrada")
        
        print("\n5. Verificando permisos y roles...")
        
        # Verificar que existen las verificaciones de permisos
        if 'auth.has_membership' in controller_content:
            print("   ✅ Verificación de permisos encontrada")
        else:
            print("   ❌ Verificación de permisos NO encontrada")
        
        print("\n6. Resumen del diagnóstico:")
        
        if not elementos_faltantes and controller_ok:
            print("   ✅ El formulario de registro parece estar completo")
            print("   📝 Posibles causas del problema:")
            print("      - Permisos de usuario (debe ser administrador u operador)")
            print("      - Errores de JavaScript en el navegador")
            print("      - Problemas de conexión a la base de datos")
            print("      - Errores en el servidor web2py")
        else:
            print("   ❌ Se encontraron problemas en el formulario")
            print("   🔧 Requiere corrección de los elementos faltantes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_registro_cliente()