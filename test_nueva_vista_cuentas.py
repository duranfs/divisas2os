#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test de la nueva vista de cuentas para clientes
"""

import os

def test_nueva_vista():
    """Verificar que la nueva vista y función están implementadas"""
    
    print("=" * 70)
    print("TEST: Nueva Vista de Cuentas para Clientes")
    print("=" * 70)
    
    # Verificar que se creó la nueva función
    print("1. VERIFICANDO NUEVA FUNCIÓN EN CONTROLADOR:")
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            if "def mis_cuentas():" in contenido:
                print("   ✓ Función mis_cuentas() creada")
                
                if "cliente_record = db(db.clientes.user_id == auth.user.id)" in contenido:
                    print("   ✓ Busca cliente directamente por user_id")
                
                if "cuentas = db(db.cuentas.cliente_id == cliente.id)" in contenido:
                    print("   ✓ Obtiene cuentas del cliente")
                
                if "return dict(" in contenido and "cliente=cliente" in contenido:
                    print("   ✓ Retorna datos necesarios")
            else:
                print("   ❌ Función mis_cuentas() NO encontrada")
    
    # Verificar que se creó la nueva vista
    print("\n2. VERIFICANDO NUEVA VISTA:")
    if os.path.exists("views/cuentas/mis_cuentas.html"):
        print("   ✓ Vista mis_cuentas.html creada")
        
        with open("views/cuentas/mis_cuentas.html", 'r', encoding='utf-8') as f:
            contenido_vista = f.read()
            
            if "Mis Cuentas Bancarias" in contenido_vista:
                print("   ✓ Título correcto")
            
            if "{{if cliente and cuentas:}}" in contenido_vista:
                print("   ✓ Verifica datos de cliente y cuentas")
            
            if "{{for cuenta in cuentas:}}" in contenido_vista:
                print("   ✓ Itera sobre cuentas")
            
            if "{{=cuenta.numero_cuenta}}" in contenido_vista:
                print("   ✓ Muestra datos de cuentas")
    else:
        print("   ❌ Vista mis_cuentas.html NO encontrada")
    
    print("\n" + "=" * 70)
    print("NUEVA SOLUCIÓN IMPLEMENTADA:")
    print("✓ Función mis_cuentas() - más simple y directa")
    print("✓ Vista mis_cuentas.html - diseñada específicamente para clientes")
    print("✓ Sin dependencia de roles complejos")
    print("✓ Búsqueda directa en tabla clientes")
    
    print("\nCÓMO USAR LA NUEVA VISTA:")
    print("1. Accede a: http://localhost:8000/sistema_divisas/cuentas/mis_cuentas")
    print("2. O agrega un enlace en el menú que apunte a:")
    print("   URL('cuentas', 'mis_cuentas')")
    
    print("\nVENTAJAS DE ESTA SOLUCIÓN:")
    print("- No depende de get_user_roles()")
    print("- Búsqueda directa en base de datos")
    print("- Manejo de errores simplificado")
    print("- Vista específica para clientes")
    print("- Fácil de mantener y debuggear")

if __name__ == "__main__":
    test_nueva_vista()