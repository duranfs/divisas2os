#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para corregir cuentas duplicadas
Consolida saldos y desactiva cuentas duplicadas
"""

print("="*80)
print("CORRIGIENDO CUENTAS DUPLICADAS")
print("="*80)

try:
    # Buscar clientes con cuentas duplicadas
    duplicados = db.executesql('''
        SELECT cliente_id, moneda, COUNT(*) as cnt 
        FROM cuentas 
        WHERE estado='activa' 
        GROUP BY cliente_id, moneda 
        HAVING COUNT(*) > 1
    ''')
    
    print(f"\nEncontrados {len(duplicados)} casos de cuentas duplicadas")
    
    for cliente_id, moneda, cnt in duplicados:
        print(f"\n[Cliente {cliente_id}, Moneda {moneda}]: {cnt} cuentas activas")
        
        # Obtener todas las cuentas duplicadas
        cuentas = db(
            (db.cuentas.cliente_id == cliente_id) &
            (db.cuentas.moneda == moneda) &
            (db.cuentas.estado == 'activa')
        ).select(orderby=db.cuentas.id)
        
        # Mantener la primera cuenta y consolidar saldos
        cuenta_principal = cuentas.first()
        saldo_total = sum([float(c.saldo or 0) for c in cuentas])
        
        print(f"  Cuenta principal: {cuenta_principal.numero_cuenta}")
        print(f"  Saldo total consolidado: {saldo_total:.2f} {moneda}")
        
        # Actualizar saldo de cuenta principal
        cuenta_principal.update_record(saldo=saldo_total)
        
        # Desactivar las demás cuentas
        for cuenta in cuentas[1:]:
            print(f"  Desactivando cuenta duplicada: {cuenta.numero_cuenta} (Saldo: {cuenta.saldo})")
            cuenta.update_record(estado='inactiva')
    
    db.commit()
    
    print("\n" + "="*80)
    print("CORRECCION COMPLETADA")
    print("="*80)
    print(f"\nSe corrigieron {len(duplicados)} casos de cuentas duplicadas")
    print("Los saldos fueron consolidados en las cuentas principales")
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
    db.rollback()
    import traceback
    traceback.print_exc()
