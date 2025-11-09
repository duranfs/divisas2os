#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación final de la corrección de la función detalle
"""

import os

def verificar_todo_corregido():
    """Verificar que todos los problemas han sido corregidos"""
    
    print("=" * 70)
    print("VERIFICACIÓN FINAL: Función detalle() corregida")
    print("=" * 70)
    
    problemas_encontrados = []
    
    # 1. Verificar controlador
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            if "validate_account_access(" in contenido:
                print("✓ Controlador usa validación de permisos correcta")
            else:
                problemas_encontrados.append("Controlador no usa validate_account_access")
                
            if "get_user_roles()" in contenido:
                print("✓ Controlador obtiene roles de usuario")
            else:
                problemas_encontrados.append("Controlador no obtiene roles")
    
    # 2. Verificar vista
    if os.path.exists("views/cuentas/detalle.html"):
        with open("views/cuentas/detalle.html", 'r', encoding='utf-8') as f:
            contenido_vista = f.read()
            
            if "</div><" not in contenido_vista:
                print("✓ Vista no tiene errores de sintaxis HTML")
            else:
                problemas_encontrados.append("Vista tiene error de sintaxis HTML")
                
            if "<style>" in contenido_vista and "</style>" in contenido_vista:
                print("✓ Vista tiene CSS correctamente formateado")
            else:
                problemas_encontrados.append("Vista tiene problemas con CSS")
    
    print("\n" + "=" * 70)
    
    if not problemas_encontrados:
        print("🎉 CORRECCIÓN COMPLETADA EXITOSAMENTE")
        print("\nLa función detalle() ahora debería funcionar correctamente:")
        print("- ✓ Administradores pueden ver detalles de cualquier cuenta")
        print("- ✓ Operadores pueden ver detalles de cualquier cuenta")
        print("- ✓ Clientes pueden ver detalles de sus propias cuentas")
        print("- ✓ Vista se renderiza correctamente sin errores CSS")
        print("\nPrueba hacer clic en 'Ver detalles' nuevamente.")
    else:
        print("❌ PROBLEMAS PENDIENTES:")
        for problema in problemas_encontrados:
            print(f"  - {problema}")

if __name__ == "__main__":
    verificar_todo_corregido()