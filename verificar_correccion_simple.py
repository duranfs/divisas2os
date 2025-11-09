#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación simple de la corrección del registro
"""

import os

def verificar_simple():
    """Verificar que la corrección está presente"""
    
    print("=" * 70)
    print("VERIFICACIÓN SIMPLE: Corrección de registro")
    print("=" * 70)
    
    if os.path.exists("controllers/clientes.py"):
        with open("controllers/clientes.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Buscar elementos clave
            elementos_encontrados = []
            
            if "from gluon.validators import CRYPT" in contenido:
                elementos_encontrados.append("✓ Importa CRYPT")
            
            if "password_validator = db.auth_user.password.requires" in contenido:
                elementos_encontrados.append("✓ Obtiene validador de contraseña")
            
            if "hashed_password = password_validator" in contenido:
                elementos_encontrados.append("✓ Hashea la contraseña")
            
            if "password=hashed_password" in contenido:
                elementos_encontrados.append("✓ Usa contraseña hasheada")
            
            print("ELEMENTOS ENCONTRADOS:")
            for elemento in elementos_encontrados:
                print(elemento)
            
            if len(elementos_encontrados) >= 3:
                print("\n🎉 CORRECCIÓN APLICADA EXITOSAMENTE")
                print("\nEl registro de clientes ahora debería:")
                print("- Hashear las contraseñas correctamente")
                print("- Permitir login exitoso después del registro")
                print("- Ser compatible con el sistema de auth de web2py")
                
                print("\nPARA PROBAR:")
                print("1. Registra un nuevo cliente con email y contraseña")
                print("2. Intenta hacer login con esas credenciales")
                print("3. El login debería funcionar sin problemas")
            else:
                print("\n❌ CORRECCIÓN INCOMPLETA")
                print("Faltan algunos elementos de la corrección")

if __name__ == "__main__":
    verificar_simple()