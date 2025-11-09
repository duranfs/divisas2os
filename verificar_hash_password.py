#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que el hash de contraseña está implementado correctamente
"""

import os

def verificar_hash_correcto():
    """Verificar que el hash de contraseña fue corregido"""
    
    print("=" * 70)
    print("VERIFICACIÓN: Hash de contraseña en registro")
    print("=" * 70)
    
    if os.path.exists("controllers/clientes.py"):
        with open("controllers/clientes.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            print("BUSCANDO IMPLEMENTACIÓN DE HASH:")
            
            # Verificar que importa CRYPT
            if "from gluon.validators import CRYPT" in contenido:
                print("✓ Importa CRYPT de gluon.validators")
            else:
                print("❌ NO importa CRYPT")
            
            # Verificar que usa password_validator
            if "password_validator = db.auth_user.password.requires" in contenido:
                print("✓ Obtiene validador de contraseña de auth_user")
            else:
                print("❌ NO obtiene validador de contraseña")
            
            # Verificar que hashea la contraseña
            if "hashed_password = password_validator(request.vars.password)[0]" in contenido:
                print("✓ Hashea la contraseña correctamente")
            else:
                print("❌ NO hashea la contraseña")
            
            # Verificar que usa la contraseña hasheada
            if "password=hashed_password," in contenido:
                print("✓ Usa contraseña hasheada en insert")
            else:
                print("❌ NO usa contraseña hasheada")
            
            # Mostrar fragmento relevante
            inicio = contenido.find("# Crear usuario con contraseña")
            if inicio != -1:
                fin = contenido.find("# Crear registro en tabla clientes", inicio)
                if fin != -1:
                    fragmento = contenido[inicio:fin]
                    print("\nFRAGMENTO DE CÓDIGO ACTUAL:")
                    print("-" * 50)
                    print(fragmento[:500] + "..." if len(fragmento) > 500 else fragmento)
                    print("-" * 50)
    
    print("\n" + "=" * 70)
    print("DIAGNÓSTICO:")
    print("Si todos los elementos están marcados con ✓, el hash")
    print("de contraseña debería funcionar correctamente.")

if __name__ == "__main__":
    verificar_hash_correcto()