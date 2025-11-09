#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que la corrección de la función detalle() funciona
"""

import os

def verificar_correccion():
    """Verificar que la función detalle fue corregida correctamente"""
    
    print("=" * 70)
    print("VERIFICACIÓN: Corrección de función detalle()")
    print("=" * 70)
    
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Buscar la función detalle corregida
            inicio = contenido.find("def detalle():")
            if inicio != -1:
                siguiente_def = contenido.find("\ndef ", inicio + 1)
                if siguiente_def == -1:
                    siguiente_def = len(contenido)
                
                funcion_detalle = contenido[inicio:siguiente_def]
                
                print("VERIFICANDO CORRECCIONES:")
                
                # Verificar que usa validate_account_access
                if "validate_account_access(" in funcion_detalle:
                    print("✓ Usa función validate_account_access() para permisos")
                else:
                    print("❌ NO usa validate_account_access()")
                
                # Verificar que obtiene roles de usuario
                if "get_user_roles()" in funcion_detalle:
                    print("✓ Obtiene roles de usuario correctamente")
                else:
                    print("❌ NO obtiene roles de usuario")
                
                # Verificar que no tiene validación restrictiva de cliente
                if "cliente = db(db.clientes.user_id == auth.user.id)" not in funcion_detalle:
                    print("✓ Eliminada validación restrictiva de cliente")
                else:
                    print("❌ Aún tiene validación restrictiva")
                
                # Verificar que obtiene cliente de la cuenta
                if "cliente = db(db.clientes.id == cuenta.cliente_id)" in funcion_detalle:
                    print("✓ Obtiene cliente asociado a la cuenta")
                else:
                    print("❌ NO obtiene cliente de la cuenta")
                
                print("\n" + "=" * 70)
                print("RESULTADO:")
                
                elementos_correctos = [
                    "validate_account_access(" in funcion_detalle,
                    "get_user_roles()" in funcion_detalle,
                    "cliente = db(db.clientes.user_id == auth.user.id)" not in funcion_detalle,
                    "cliente = db(db.clientes.id == cuenta.cliente_id)" in funcion_detalle
                ]
                
                if all(elementos_correctos):
                    print("🎉 CORRECCIÓN EXITOSA")
                    print("La función detalle() ahora debería funcionar para:")
                    print("- Administradores (pueden ver cualquier cuenta)")
                    print("- Operadores (pueden ver cualquier cuenta)")
                    print("- Clientes (pueden ver solo sus cuentas)")
                else:
                    print("❌ CORRECCIÓN INCOMPLETA")
                    print("Algunos elementos no están corregidos correctamente")
                
            else:
                print("❌ No se encontró la función detalle()")
    else:
        print("❌ No se encontró el archivo controllers/cuentas.py")

if __name__ == "__main__":
    verificar_correccion()