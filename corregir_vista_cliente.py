#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para corregir definitivamente la vista de cliente
"""

def crear_solucion_simple():
    """Crear una solución simple que funcione"""
    
    print("=" * 70)
    print("🔧 CORRECCIÓN DEFINITIVA: Vista de Cliente")
    print("=" * 70)
    
    print("PROBLEMA IDENTIFICADO:")
    print("- Los clientes no ven nada cuando acceden a sus cuentas")
    print("- La función index() tiene lógica compleja que falla")
    print("- Hay problemas con roles y redirecciones")
    
    print("\nSOLUCIÓN SIMPLE:")
    print("Vamos a crear una función debug_cliente() que:")
    print("1. Muestre información básica del usuario")
    print("2. Verifique si existe como cliente")
    print("3. Muestre sus cuentas si las tiene")
    print("4. No dependa de roles complejos")
    
    # Código para la función debug
    codigo_funcion = '''
@auth.requires_login()
def debug_cliente():
    """Función de debug para clientes - sin dependencias complejas"""
    
    # Información básica del usuario
    usuario_info = {
        'user_id': auth.user.id if auth.user else None,
        'email': auth.user.email if auth.user else None,
        'first_name': auth.user.first_name if auth.user else None,
        'last_name': auth.user.last_name if auth.user else None
    }
    
    # Buscar si es cliente
    cliente_record = None
    try:
        cliente_record = db(db.clientes.user_id == auth.user.id).select().first()
    except:
        pass
    
    # Buscar cuentas si es cliente
    cuentas = []
    if cliente_record:
        try:
            cuentas = db(db.cuentas.cliente_id == cliente_record.id).select()
        except:
            pass
    
    # Calcular totales simples
    total_ves = 0
    total_usd = 0
    total_eur = 0
    
    for cuenta in cuentas:
        try:
            total_ves += float(cuenta.saldo_ves or 0)
            total_usd += float(cuenta.saldo_usd or 0)
            total_eur += float(cuenta.saldo_eur or 0)
        except:
            pass
    
    return dict(
        usuario_info=usuario_info,
        cliente_record=cliente_record,
        cuentas=cuentas,
        total_ves=total_ves,
        total_usd=total_usd,
        total_eur=total_eur,
        num_cuentas=len(cuentas)
    )
'''
    
    print("\nCÓDIGO DE LA FUNCIÓN:")
    print("-" * 50)
    print(codigo_funcion)
    print("-" * 50)
    
    print("\nVISTA SIMPLE NECESARIA:")
    print("- Archivo: views/cuentas/debug_cliente.html")
    print("- Mostrar información del usuario")
    print("- Mostrar si es cliente o no")
    print("- Mostrar cuentas si las tiene")
    print("- Mostrar totales básicos")
    
    print("\nPARA USAR:")
    print("1. Agregar la función al controlador")
    print("2. Crear la vista debug_cliente.html")
    print("3. Acceder a /cuentas/debug_cliente")
    print("4. Ver qué información aparece")
    
    print("\n" + "=" * 70)
    print("Esta función de debug nos ayudará a identificar")
    print("exactamente qué datos tiene el cliente y por qué")
    print("no se muestran en la vista principal.")

if __name__ == "__main__":
    crear_solucion_simple()