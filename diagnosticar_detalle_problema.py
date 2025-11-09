#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnosticar problema con función detalle() de cuentas
"""

import os

def diagnosticar_problema_detalle():
    """Analizar la función detalle para identificar el problema de permisos"""
    
    print("=" * 70)
    print("DIAGNÓSTICO: Problema con función detalle() de cuentas")
    print("=" * 70)
    
    # Leer la función detalle actual
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Buscar la función detalle
            inicio = contenido.find("def detalle():")
            if inicio != -1:
                # Encontrar el final de la función (próxima función o final de archivo)
                siguiente_def = contenido.find("\ndef ", inicio + 1)
                if siguiente_def == -1:
                    siguiente_def = len(contenido)
                
                funcion_detalle = contenido[inicio:siguiente_def]
                
                print("FUNCIÓN DETALLE ACTUAL:")
                print("-" * 50)
                print(funcion_detalle[:1000] + "..." if len(funcion_detalle) > 1000 else funcion_detalle)
                print("-" * 50)
                
                # Analizar problemas potenciales
                print("\nANÁLISIS DE PROBLEMAS:")
                
                if "cliente = db(db.clientes.user_id == auth.user.id)" in funcion_detalle:
                    print("❌ PROBLEMA IDENTIFICADO:")
                    print("   La función solo permite acceso a clientes registrados")
                    print("   Si eres administrador, no tienes registro como cliente")
                    print("   Esto causa el error 'acceso no autorizado'")
                
                if "(db.cuentas.cliente_id == cliente.id)" in funcion_detalle:
                    print("❌ PROBLEMA IDENTIFICADO:")
                    print("   La función solo muestra cuentas del cliente actual")
                    print("   Los administradores necesitan ver cualquier cuenta")
                
                print("\nSOLUCIÓN REQUERIDA:")
                print("✓ Modificar la función para permitir acceso de administradores")
                print("✓ Usar la función validate_account_access() que ya existe")
                print("✓ Permitir que administradores vean cualquier cuenta")
                
            else:
                print("❌ No se encontró la función detalle()")
    else:
        print("❌ No se encontró el archivo controllers/cuentas.py")

if __name__ == "__main__":
    diagnosticar_problema_detalle()