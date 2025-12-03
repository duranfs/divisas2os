#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test simple de vender
"""

print("="*80)
print("TEST SIMPLE VENDER")
print("="*80)

try:
    # Buscar cliente
    print("\n[1] Buscando cliente...")
    cliente = db(db.clientes).select(limitby=(0,1)).first()
    
    if not cliente:
        print("  ERROR: No hay clientes")
    else:
        print(f"  Cliente: {cliente.cedula}")
        
        # Buscar cuentas
        print("\n[2] Buscando cuentas...")
        cuentas = db(
            (db.cuentas.cliente_id == cliente.id) &
            (db.cuentas.estado == 'activa')
        ).select()
        
        print(f"  Total: {len(cuentas)}")
        for c in cuentas:
            print(f"    {c.moneda}: {c.saldo}")
        
        # Buscar cuenta USD con saldo
        cuenta_usd = None
        for c in cuentas:
            if c.moneda == 'USD' and c.saldo > 0:
                cuenta_usd = c
                break
        
        if cuenta_usd:
            print(f"\n[3] Cuenta USD encontrada: {cuenta_usd.saldo} USD")
            print("  Sistema listo para vender")
        else:
            print("\n[3] No hay cuenta USD con saldo")
            
except Exception as e:
    print(f"\nERROR: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n"+"="*80)
