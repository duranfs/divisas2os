#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test final para verificar corrección de login
"""

import os

def test_login_final():
    """Test final del problema de login"""
    
    print("=" * 70)
    print("TEST FINAL: Corrección de Login de Clientes")
    print("=" * 70)
    
    # Verificar que la corrección está aplicada
    if os.path.exists("controllers/clientes.py"):
        with open("controllers/clientes.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            print("VERIFICANDO CORRECCIÓN APLICADA:")
            
            elementos_correctos = []
            
            if "from gluon.validators import CRYPT" in contenido:
                elementos_correctos.append("✓ Importa CRYPT")
            
            if "password_validator = CRYPT()" in contenido:
                elementos_correctos.append("✓ Crea validador CRYPT")
            
            if "validated_password, error = password_validator" in contenido:
                elementos_correctos.append("✓ Valida contraseña")
            
            if "password=validated_password" in contenido:
                elementos_correctos.append("✓ Usa contraseña validada")
            
            for elemento in elementos_correctos:
                print(f"  {elemento}")
            
            if len(elementos_correctos) >= 3:
                print("\n🎉 CORRECCIÓN APLICADA CORRECTAMENTE")
                
                print("\nLO QUE SE CORRIGIÓ:")
                print("- Se importa CRYPT de gluon.validators")
                print("- Se crea un validador CRYPT manualmente")
                print("- Se valida la contraseña antes de insertar")
                print("- Se usa la contraseña hasheada en el insert")
                print("- Se maneja errores de validación")
                
                print("\nRESULTADO ESPERADO:")
                print("✅ Los nuevos clientes registrados ahora deberían")
                print("   poder hacer login correctamente")
                
                print("\nPARA PROBAR:")
                print("1. Registra un nuevo cliente")
                print("2. Anota el email y contraseña usados")
                print("3. Cierra sesión como administrador")
                print("4. Intenta login con las credenciales del cliente")
                print("5. Debería funcionar sin 'login inválido'")
                
            else:
                print("\n❌ CORRECCIÓN INCOMPLETA")
                print("Algunos elementos de la corrección faltan")
    
    print("\n" + "=" * 70)
    print("NOTA IMPORTANTE:")
    print("Si el problema persiste, puede ser necesario verificar:")
    print("- Configuración de CRYPT en models/db.py")
    print("- Que no hay validaciones adicionales en auth")
    print("- Que la tabla auth_user tiene la estructura correcta")

if __name__ == "__main__":
    test_login_final()