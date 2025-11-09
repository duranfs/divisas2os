#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test final del historial de transacciones
"""

import os

def test_historial_completo():
    """Test completo de la funcionalidad de historial"""
    
    print("=" * 70)
    print("TEST FINAL: Historial de Transacciones")
    print("=" * 70)
    
    # Verificar todos los componentes
    componentes = {
        "Función historial_transacciones": False,
        "Función get_user_roles": False,
        "Vista historial_transacciones.html": False,
        "Enlace corregido en detalle.html": False
    }
    
    # 1. Verificar controlador divisas
    if os.path.exists("controllers/divisas.py"):
        with open("controllers/divisas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            if "def historial_transacciones():" in contenido:
                componentes["Función historial_transacciones"] = True
                
            if "def get_user_roles(" in contenido:
                componentes["Función get_user_roles"] = True
    
    # 2. Verificar vista
    if os.path.exists("views/divisas/historial_transacciones.html"):
        componentes["Vista historial_transacciones.html"] = True
    
    # 3. Verificar enlace
    if os.path.exists("views/cuentas/detalle.html"):
        with open("views/cuentas/detalle.html", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "URL('divisas', 'historial_transacciones')" in contenido:
                componentes["Enlace corregido en detalle.html"] = True
    
    # Mostrar resultados
    for componente, estado in componentes.items():
        if estado:
            print(f"✓ {componente}")
        else:
            print(f"❌ {componente}")
    
    print("\n" + "=" * 70)
    
    if all(componentes.values()):
        print("🎉 TODOS LOS COMPONENTES ESTÁN LISTOS")
        print("\nEl botón 'Ver Historial Completo' debería funcionar ahora.")
        print("Si aún no funciona, verifica:")
        print("1. Que el servidor web2py esté ejecutándose")
        print("2. Que no haya errores en los logs de web2py")
        print("3. Que la base de datos esté accesible")
    else:
        print("❌ FALTAN COMPONENTES")
        print("Revisa los elementos marcados con ❌")

if __name__ == "__main__":
    test_historial_completo()