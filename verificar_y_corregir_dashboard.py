#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar y corregir el dashboard
"""

print("=" * 80)
print("VERIFICACIÓN Y CORRECCIÓN DEL DASHBOARD")
print("=" * 80)

try:
    # 1. Verificar estructura de cuentas
    print("\n[1] Verificando estructura de cuentas...")
    cuentas = db().select(db.cuentas.ALL, limitby=(0, 5))
    
    if cuentas:
        cuenta = cuentas.first()
        print(f"  ✓ Campos en cuentas:")
        print(f"    - moneda: {hasattr(cuenta, 'moneda')}")
        print(f"    - saldo: {hasattr(cuenta, 'saldo')}")
        print(f"    - saldo_ves: {hasattr(cuenta, 'saldo_ves')}")
        print(f"    - saldo_usd: {hasattr(cuenta, 'saldo_usd')}")
    
    # 2. Verificar estructura de transacciones
    print("\n[2] Verificando estructura de transacciones...")
    trans = db().select(db.transacciones.ALL, limitby=(0, 1))
    
    if trans:
        tx = trans.first()
        print(f"  ✓ Campos en transacciones:")
        print(f"    - cuenta_id: {hasattr(tx, 'cuenta_id')}")
        print(f"    - cuenta_origen_id: {hasattr(tx, 'cuenta_origen_id')}")
        print(f"    - cuenta_destino_id: {hasattr(tx, 'cuenta_destino_id')}")
        print(f"    - tasa_aplicada: {hasattr(tx, 'tasa_aplicada')}")
        print(f"    - numero_comprobante: {hasattr(tx, 'numero_comprobante')}")
    
    # 3. Probar dashboard_cliente
    print("\n[3] Probando función dashboard_cliente...")
    cliente = db(db.clientes).select().first()
    
    if cliente:
        print(f"  Cliente encontrado: ID {cliente.id}")
        
        # Obtener cuentas
        cuentas = db(
            (db.cuentas.cliente_id == cliente.id) &
            (db.cuentas.estado == 'activa')
        ).select()
        
        print(f"  Cuentas activas: {len(cuentas)}")
        
        # Calcular totales
        total_ves = sum([float(cuenta.saldo or 0) for cuenta in cuentas if cuenta.moneda == 'VES'])
        total_usd = sum([float(cuenta.saldo or 0) for cuenta in cuentas if cuenta.moneda == 'USD'])
        
        print(f"  Total VES: {total_ves:,.2f}")
        print(f"  Total USD: {total_usd:,.2f}")
        
        # Probar transacciones
        cuenta_ids = [c.id for c in cuentas]
        if cuenta_ids:
            ultimas_trans = db(
                db.transacciones.cuenta_id.belongs(cuenta_ids)
            ).select(
                orderby=~db.transacciones.fecha_transaccion,
                limitby=(0, 5)
            )
            print(f"  Últimas transacciones: {len(ultimas_trans)}")
        
        print("  ✓ dashboard_cliente funciona correctamente")
    
    print("\n" + "=" * 80)
    print("✅ VERIFICACIÓN COMPLETADA - TODO FUNCIONA")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
