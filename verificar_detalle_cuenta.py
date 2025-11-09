#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar que la funcionalidad de detalles de cuenta funciona correctamente
"""

import sys
import os

# Agregar el directorio de web2py al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def verificar_detalle_cuenta():
    """Verificar que la vista y controlador de detalles de cuenta están implementados"""
    
    print("=" * 60)
    print("VERIFICACIÓN: Funcionalidad de Detalles de Cuenta")
    print("=" * 60)
    
    # 1. Verificar que existe el controlador
    controlador_path = "controllers/cuentas.py"
    if os.path.exists(controlador_path):
        print("✓ Controlador cuentas.py existe")
        
        # Verificar función detalle
        with open(controlador_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'def detalle():' in contenido:
                print("✓ Función detalle() implementada en controlador")
                
                # Verificar elementos clave de la función
                elementos_requeridos = [
                    'cuenta_id = request.args(0)',
                    'cliente = db(db.clientes.user_id == auth.user.id)',
                    'cuenta = db(',
                    'ultimas_transacciones = db(',
                    'estadisticas_mes = {'
                ]
                
                for elemento in elementos_requeridos:
                    if elemento in contenido:
                        print(f"  ✓ {elemento}")
                    else:
                        print(f"  ✗ FALTA: {elemento}")
            else:
                print("✗ Función detalle() NO encontrada en controlador")
    else:
        print("✗ Controlador cuentas.py NO existe")
    
    # 2. Verificar que existe la vista
    vista_path = "views/cuentas/detalle.html"
    if os.path.exists(vista_path):
        print("✓ Vista detalle.html existe")
        
        with open(vista_path, 'r', encoding='utf-8') as f:
            contenido_vista = f.read()
            
            # Verificar elementos clave de la vista
            elementos_vista = [
                "{{extend 'layout.html'}}",
                "Detalles de Cuenta",
                "{{if cuenta and cliente:}}",
                "Información de la Cuenta",
                "Saldos Actuales",
                "Últimas Transacciones",
                "{{=cuenta.numero_cuenta}}",
                "{{=cuenta.saldo_ves}}",
                "{{=cuenta.saldo_usd}}",
                "{{=cuenta.saldo_eur}}"
            ]
            
            for elemento in elementos_vista:
                if elemento in contenido_vista:
                    print(f"  ✓ {elemento}")
                else:
                    print(f"  ✗ FALTA: {elemento}")
    else:
        print("✗ Vista detalle.html NO existe")
    
    # 3. Verificar que el enlace está en la vista de listado
    vista_listar_path = "views/cuentas/index.html"
    if os.path.exists(vista_listar_path):
        print("✓ Vista index.html existe")
        
        with open(vista_listar_path, 'r', encoding='utf-8') as f:
            contenido_index = f.read()
            
            if "URL('cuentas', 'detalle'" in contenido_index:
                print("  ✓ Enlace a detalle encontrado en vista index")
            else:
                print("  ✗ Enlace a detalle NO encontrado en vista index")
    else:
        print("✗ Vista index.html NO existe")
    
    print("\n" + "=" * 60)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    print("La funcionalidad de detalles de cuenta debería estar completamente")
    print("implementada si todos los elementos anteriores están marcados con ✓")
    print("\nPara probar:")
    print("1. Inicia el servidor web2py")
    print("2. Ve a 'Mis Cuentas'")
    print("3. Haz clic en 'Ver detalles' de cualquier cuenta")
    print("4. Deberías ver información completa de la cuenta")

if __name__ == "__main__":
    verificar_detalle_cuenta()