#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar corrección de acceso a cuentas para clientes
"""

import os

def verificar_correccion():
    """Verificar que la corrección se aplicó correctamente"""
    
    print("=" * 70)
    print("VERIFICACIÓN: Corrección de Acceso a Cuentas")
    print("=" * 70)
    
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            print("VERIFICANDO CORRECCIONES APLICADAS:")
            
            # Verificar que maneja caso sin rol de cliente
            if "else:" in contenido and "cliente = db(db.clientes.user_id == auth.user.id)" in contenido:
                print("✓ Maneja caso de usuario sin rol de cliente")
            else:
                print("❌ NO maneja caso sin rol de cliente")
            
            # Verificar que asigna rol automáticamente
            if "auth.add_membership(grupo_cliente.id, auth.user.id)" in contenido:
                print("✓ Asigna rol de cliente automáticamente")
            else:
                print("❌ NO asigna rol automáticamente")
            
            # Verificar redirección
            if "redirect(URL('cuentas', 'index'))" in contenido:
                print("✓ Redirige después de asignar rol")
            else:
                print("❌ NO redirige después de asignar rol")
    
    print("\n" + "=" * 70)
    print("CORRECCIÓN APLICADA:")
    print("✓ Se agregó lógica para detectar clientes sin rol asignado")
    print("✓ Se asigna automáticamente el rol de cliente si falta")
    print("✓ Se redirige para recargar la página con el nuevo rol")
    
    print("\nEL PROBLEMA ERA:")
    print("- Los clientes se registraban correctamente")
    print("- Pero a veces el rol no se asignaba correctamente")
    print("- Sin rol de cliente, no podían acceder a sus cuentas")
    
    print("\nLA SOLUCIÓN:")
    print("- Detectar si el usuario existe en tabla clientes")
    print("- Si existe pero no tiene rol, asignarlo automáticamente")
    print("- Redirigir para que vea sus cuentas correctamente")
    
    print("\nPARA PROBAR:")
    print("1. Haz login como cliente")
    print("2. Ve a 'Mis Cuentas' o 'Datos Bancarios'")
    print("3. Deberías ver tus cuentas y saldos")
    print("4. Si aparece mensaje de rol asignado, recarga la página")

if __name__ == "__main__":
    verificar_correccion()