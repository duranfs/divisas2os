#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test directo de la función vender
"""

print("="*80)
print("TEST DIRECTO DE VENDER")
print("="*80)

try:
    # Simular usuario autenticado
    print("\n[1] Verificando usuario autenticado...")
    if auth.user:
        print(f"  Usuario: {auth.user.email}")
        print(f"  ID: {auth.user.id}")
    else:
        print("  No hay usuario autenticado (modo test)")
        
    # Buscar cliente
    print("\n[2] Buscando cliente...")
    if auth.user:
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
    else:
        cliente = None
        
    if not cliente:
        print("  Buscando cualquier cliente...")
        cliente = db(db.clientes).select(limitby=(0,1)).first()
    
    if cliente:
        print(f"  Cliente ID: {cliente.id}")
        print(f"  Cedula: {cliente.cedula}")
    else:
        print("  ERROR: No hay clientes en el sistema")
        
    # Buscar cuentas
    print("\n[3] Buscando cuentas del cliente...")
    cuentas = db(
        (db.cuentas.cliente_id == cliente.id) &
        (db.cuentas.estado == 'activa')
    ).select()
    
    print(f"  Total cuentas: {len(cuentas)}")
    for cuenta in cuentas:
        print(f"    - {cuenta.moneda}: {cuenta.numero_cuenta} - Saldo: {cuenta.saldo}")
    
    # Verificar tasas
    print("\n[4] Verificando tasas...")
    tasas = obtener_tasas_actuales()
    if tasas:
        print(f"  USD/VES: {tasas.usd_ves}")
        print(f"  EUR/VES: {tasas.eur_ves}")
    else:
        print("  ERROR: No hay tasas")
    
    # Simular venta
    print("\n[5] Simulando venta de 10 USD...")
    
    # Buscar cuenta USD
    cuenta_usd = None
    for cuenta in cuentas:
        if cuenta.moneda == 'USD':
            cuenta_usd = cuenta
            break
    
    if not cuenta_usd:
        print("  ERROR: No hay cuenta USD")
    else:
        print(f"  Cuenta USD: {cuenta_usd.numero_cuenta}")
        print(f"  Saldo actual: {cuenta_usd.saldo} USD")
        
        if cuenta_usd.saldo >= 10:
            print("  Saldo suficiente para vender 10 USD")
            
            # Simular los parámetros que enviaría el formulario
            from gluon.storage import Storage
            request.vars = Storage()
            request.vars.cuenta_id = cuenta_usd.id
            request.vars.moneda_origen = 'USD'
            request.vars.cantidad_divisa = '10'
            request.vars.confirmar_venta = True
            
            print("\n[6] Llamando a procesar_venta_divisa()...")
            resultado = procesar_venta_divisa()
            
            if resultado['success']:
                print("  EXITO!")
                print(f"    Comprobante: {resultado['comprobante']}")
                print(f"    Monto origen: {resultado['monto_origen']} USD")
                print(f"    Monto destino: {resultado['monto_destino']} VES")
                print(f"    Tasa: {resultado['tasa_aplicada']}")
            else:
                print(f"  ERROR: {resultado['error']}")
        else:
            print(f"  ERROR: Saldo insuficiente ({cuenta_usd.saldo} USD)")
    
except Exception as e:
    print(f"\nERROR GENERAL: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n"+"="*80)
print("TEST COMPLETADO")
print("="*80)
