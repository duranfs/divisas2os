#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnosticar problemas con el historial de transacciones
"""

import os

def diagnosticar_historial():
    """Diagnosticar posibles problemas con historial_transacciones"""
    
    print("=" * 70)
    print("DIAGNÓSTICO: Problemas con historial_transacciones")
    print("=" * 70)
    
    # 1. Verificar que la función existe
    controlador_ok = False
    if os.path.exists("controllers/divisas.py"):
        with open("controllers/divisas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "def historial_transacciones():" in contenido:
                controlador_ok = True
                print("✓ Función historial_transacciones() existe")
            else:
                print("❌ Función historial_transacciones() NO existe")
    
    # 2. Verificar que la vista existe
    vista_ok = False
    if os.path.exists("views/divisas/historial_transacciones.html"):
        vista_ok = True
        print("✓ Vista historial_transacciones.html existe")
    else:
        print("❌ Vista historial_transacciones.html NO existe")
    
    # 3. Verificar el enlace en detalle.html
    enlace_ok = False
    if os.path.exists("views/cuentas/detalle.html"):
        with open("views/cuentas/detalle.html", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "URL('divisas', 'historial_transacciones')" in contenido:
                enlace_ok = True
                print("✓ Enlace correcto en detalle.html")
            else:
                print("❌ Enlace incorrecto en detalle.html")
    
    # 4. Verificar funciones auxiliares
    funciones_ok = False
    if os.path.exists("controllers/divisas.py"):
        with open("controllers/divisas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "def get_user_roles():" in contenido:
                funciones_ok = True
                print("✓ Función get_user_roles() existe")
            else:
                print("❌ Función get_user_roles() NO existe")
    
    print("\n" + "=" * 70)
    print("POSIBLES PROBLEMAS Y SOLUCIONES:")
    
    if not controlador_ok:
        print("❌ La función historial_transacciones() no existe")
        print("   Solución: Implementar la función en controllers/divisas.py")
    
    if not vista_ok:
        print("❌ La vista historial_transacciones.html no existe")
        print("   Solución: Crear la vista en views/divisas/")
    
    if not enlace_ok:
        print("❌ El enlace en detalle.html es incorrecto")
        print("   Solución: Cambiar a URL('divisas', 'historial_transacciones')")
    
    if not funciones_ok:
        print("❌ Faltan funciones auxiliares")
        print("   Solución: Verificar que get_user_roles() existe")
    
    if controlador_ok and vista_ok and enlace_ok and funciones_ok:
        print("✅ TODOS LOS COMPONENTES ESTÁN CORRECTOS")
        print("\nSi aún no funciona, puede ser:")
        print("- Error en la base de datos (tabla transacciones vacía)")
        print("- Error de permisos de usuario")
        print("- Error en el servidor web2py")
        print("\nRevisa los logs de web2py para más detalles")

if __name__ == "__main__":
    diagnosticar_historial()