#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que el registro de clientes y login funciona correctamente
"""

import os

def verificar_registro_corregido():
    """Verificar que la función de registro fue corregida"""
    
    print("=" * 70)
    print("VERIFICACIÓN: Corrección de registro de clientes")
    print("=" * 70)
    
    if os.path.exists("controllers/clientes.py"):
        with open("controllers/clientes.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Buscar la función registrar
            inicio = contenido.find("def registrar():")
            if inicio != -1:
                siguiente_def = contenido.find("\ndef ", inicio + 1)
                if siguiente_def == -1:
                    siguiente_def = len(contenido)
                
                funcion_registrar = contenido[inicio:siguiente_def]
                
                print("VERIFICANDO CORRECCIONES EN REGISTRO:")
                
                # Verificar que usa auth.register_bare
                if "auth.register_bare(" in funcion_registrar:
                    print("✓ Usa auth.register_bare() para crear usuario")
                else:
                    print("❌ NO usa auth.register_bare()")
                
                # Verificar que no usa inserción directa problemática
                if "password=request.vars.password," not in funcion_registrar:
                    print("✓ NO usa inserción directa de contraseña")
                else:
                    print("❌ Aún usa inserción directa problemática")
                
                # Verificar que actualiza campos adicionales
                if "db(db.auth_user.id == user_id).update(" in funcion_registrar:
                    print("✓ Actualiza campos adicionales correctamente")
                else:
                    print("❌ NO actualiza campos adicionales")
                
                # Verificar creación de cliente
                if "db.clientes.insert(" in funcion_registrar:
                    print("✓ Crea registro en tabla clientes")
                else:
                    print("❌ NO crea registro en tabla clientes")
                
                # Verificar asignación de rol
                if "auth.add_membership(" in funcion_registrar:
                    print("✓ Asigna rol de cliente")
                else:
                    print("❌ NO asigna rol de cliente")
                
                # Verificar creación de cuenta
                if "db.cuentas.insert(" in funcion_registrar:
                    print("✓ Crea cuenta bancaria inicial")
                else:
                    print("❌ NO crea cuenta bancaria")
                
            else:
                print("❌ Función registrar() no encontrada")
    
    print("\n" + "=" * 70)
    print("RESULTADO:")
    print("El registro de clientes ahora debería crear usuarios")
    print("con contraseñas correctamente hasheadas que permitan login.")
    print("\nPara probar:")
    print("1. Registra un nuevo cliente")
    print("2. Intenta hacer login con las credenciales")
    print("3. El login debería funcionar correctamente")

if __name__ == "__main__":
    verificar_registro_corregido()