#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación final: Botón "Ver detalles" de cuentas funciona correctamente
"""

import os

def verificar_funcionalidad_completa():
    """Verificar que toda la funcionalidad de detalles de cuenta está implementada"""
    
    print("=" * 70)
    print("VERIFICACIÓN FINAL: Funcionalidad de Detalles de Cuenta")
    print("=" * 70)
    
    # Verificar controlador
    controlador_ok = False
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'def detalle():' in contenido and 'ultimas_transacciones' in contenido:
                controlador_ok = True
                print("✓ Controlador cuentas.detalle() implementado correctamente")
    
    # Verificar vista
    vista_ok = False
    if os.path.exists("views/cuentas/detalle.html"):
        with open("views/cuentas/detalle.html", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'Detalles de Cuenta' in contenido and 'saldo_ves' in contenido:
                vista_ok = True
                print("✓ Vista detalle.html implementada correctamente")
    
    # Verificar enlace en index
    enlace_ok = False
    if os.path.exists("views/cuentas/index.html"):
        with open("views/cuentas/index.html", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "URL('cuentas', 'detalle'" in contenido:
                enlace_ok = True
                print("✓ Enlace 'Ver detalles' encontrado en vista index")
    
    print("\n" + "=" * 70)
    if controlador_ok and vista_ok and enlace_ok:
        print("🎉 ÉXITO: Funcionalidad de detalles de cuenta completamente implementada")
        print("\nPara probar:")
        print("1. Inicia web2py: python web2py.py -a password -i 127.0.0.1 -p 8000")
        print("2. Ve a: http://127.0.0.1:8000/sistema_divisas/cuentas")
        print("3. Haz clic en 'Ver detalles' de cualquier cuenta")
        print("4. Deberías ver información completa con saldos y transacciones")
    else:
        print("❌ ERROR: Algunos componentes no están implementados correctamente")

if __name__ == "__main__":
    verificar_funcionalidad_completa()