#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnóstico del error en el dashboard
"""

import sys
import os

print("=" * 80)
print("DIAGNÓSTICO DEL ERROR EN DASHBOARD")
print("=" * 80)

try:
    # Verificar estructura de la tabla cuentas
    print("\n[1] Verificando estructura de tabla cuentas...")
    
    cuentas = db().select(db.cuentas.ALL, limitby=(0, 1))
    
    if cuentas:
        cuenta = cuentas.first()
        print(f"  ✓ Tabla cuentas existe")
        print(f"  Campos disponibles:")
        for campo in cuenta.keys():
            print(f"    - {campo}: {type(cuenta[campo]).__name__}")
    else:
        print("  ⚠ No hay cuentas en la base de datos")
    
    # Verificar si existen campos antiguos
    print("\n[2] Verificando campos antiguos vs nuevos...")
    if cuentas:
        cuenta = cuentas.first()
        campos_antiguos = ['saldo_ves', 'saldo_usd', 'saldo_eur', 'saldo_usdt']
        campos_nuevos = ['moneda', 'saldo']
        
        for campo in campos_antiguos:
            if campo in cuenta:
                print(f"  ⚠ Campo antiguo '{campo}' todavía existe")
            else:
                print(f"  ✓ Campo antiguo '{campo}' eliminado")
        
        for campo in campos_nuevos:
            if campo in cuenta:
                print(f"  ✓ Campo nuevo '{campo}' existe")
            else:
                print(f"  ❌ Campo nuevo '{campo}' NO existe")
    
    # Verificar clientes
    print("\n[3] Verificando clientes...")
    clientes = db(db.clientes).select()
    print(f"  Total de clientes: {len(clientes)}")
    
    for cliente in clientes:
        print(f"\n  Cliente ID: {cliente.id}")
        print(f"    Cédula: {cliente.cedula}")
        
        # Contar cuentas por moneda
        cuentas_cliente = db(
            (db.cuentas.cliente_id == cliente.id) &
            (db.cuentas.estado == 'activa')
        ).select()
        
        print(f"    Total cuentas activas: {len(cuentas_cliente)}")
        
        if cuentas_cliente:
            for cuenta in cuentas_cliente:
                if hasattr(cuenta, 'moneda') and hasattr(cuenta, 'saldo'):
                    print(f"      • {cuenta.moneda}: {cuenta.numero_cuenta} - Saldo: {cuenta.saldo}")
                else:
                    print(f"      ⚠ Cuenta sin campos moneda/saldo: {cuenta.numero_cuenta}")
    
    # Verificar transacciones
    print("\n[4] Verificando estructura de transacciones...")
    transacciones = db().select(db.transacciones.ALL, limitby=(0, 1))
    
    if transacciones:
        tx = transacciones.first()
        print(f"  ✓ Tabla transacciones existe")
        
        campos_tx_antiguos = ['cuenta_id']
        campos_tx_nuevos = ['cuenta_origen_id', 'cuenta_destino_id']
        
        for campo in campos_tx_antiguos:
            if campo in tx:
                print(f"  ⚠ Campo antiguo '{campo}' todavía existe")
            else:
                print(f"  ✓ Campo antiguo '{campo}' eliminado")
        
        for campo in campos_tx_nuevos:
            if campo in tx:
                print(f"  ✓ Campo nuevo '{campo}' existe")
            else:
                print(f"  ❌ Campo nuevo '{campo}' NO existe")
    else:
        print("  ⚠ No hay transacciones en la base de datos")
    
    print("\n" + "=" * 80)
    print("DIAGNÓSTICO COMPLETADO")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
