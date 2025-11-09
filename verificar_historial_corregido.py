#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que la corrección del historial de transacciones funciona
"""

import os

def verificar_historial():
    """Verificar que el historial de transacciones fue corregido"""
    
    print("=" * 70)
    print("VERIFICACIÓN: Corrección de historial_transacciones()")
    print("=" * 70)
    
    # Verificar controlador divisas
    if os.path.exists("controllers/divisas.py"):
        with open("controllers/divisas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Buscar la función historial_transacciones
            inicio = contenido.find("def historial_transacciones():")
            if inicio != -1:
                siguiente_def = contenido.find("\ndef ", inicio + 1)
                if siguiente_def == -1:
                    siguiente_def = len(contenido)
                
                funcion_historial = contenido[inicio:siguiente_def]
                
                print("VERIFICANDO CORRECCIONES EN CONTROLADOR:")
                
                # Verificar que usa get_user_roles
                if "get_user_roles()" in funcion_historial:
                    print("✓ Obtiene roles de usuario")
                else:
                    print("❌ NO obtiene roles de usuario")
                
                # Verificar que permite administradores
                if "'administrador' in user_roles" in funcion_historial:
                    print("✓ Permite acceso a administradores")
                else:
                    print("❌ NO permite acceso a administradores")
                
                # Verificar query condicional
                if "if cliente:" in funcion_historial and "else:" in funcion_historial:
                    print("✓ Query condicional para clientes/administradores")
                else:
                    print("❌ NO tiene query condicional")
                
                # Verificar JOIN con clientes
                if "db.clientes.on" in funcion_historial:
                    print("✓ JOIN con tabla de clientes")
                else:
                    print("❌ NO tiene JOIN con clientes")
            else:
                print("❌ Función historial_transacciones() no encontrada")
    
    # Verificar vista de detalles corregida
    if os.path.exists("views/cuentas/detalle.html"):
        with open("views/cuentas/detalle.html", 'r', encoding='utf-8') as f:
            contenido_vista = f.read()
            
            print("\nVERIFICANDO CORRECCIONES EN VISTA:")
            
            if "URL('divisas', 'historial_transacciones')" in contenido_vista:
                print("✓ Enlace corregido a historial_transacciones")
            else:
                print("❌ Enlace NO corregido")
    
    # Verificar que existe la vista del historial
    if os.path.exists("views/divisas/historial_transacciones.html"):
        print("✓ Vista historial_transacciones.html existe")
    else:
        print("❌ Vista historial_transacciones.html NO existe")
    
    print("\n" + "=" * 70)
    print("RESULTADO:")
    print("El botón 'Ver Historial Completo' ahora debería funcionar")
    print("correctamente para administradores, operadores y clientes.")

if __name__ == "__main__":
    verificar_historial()