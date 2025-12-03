# -*- coding: utf-8 -*-
"""
Script para verificar el estado actual de la base de datos
"""

print("\n" + "=" * 80)
print("VERIFICACIÓN DEL ESTADO ACTUAL DE LA BASE DE DATOS")
print("=" * 80)

try:
    # Verificar estructura de la tabla cuentas
    print("\n1. Estructura de la tabla 'cuentas':")
    print("-" * 80)
    
    # Obtener una cuenta de ejemplo
    cuenta_ejemplo = db(db.cuentas.id > 0).select().first()
    
    if cuenta_ejemplo:
        print("\nCampos disponibles en la tabla 'cuentas':")
        for campo in db.cuentas.fields:
            valor = cuenta_ejemplo[campo] if campo in cuenta_ejemplo else 'N/A'
            tipo = db.cuentas[campo].type if hasattr(db.cuentas[campo], 'type') else 'unknown'
            print(f"   - {campo}: {tipo}")
    
    # Contar cuentas totales
    total_cuentas = db(db.cuentas.id > 0).count()
    print(f"\n2. Total de cuentas en la base de datos: {total_cuentas}")
    
    # Verificar si hay cuentas con el campo 'moneda'
    print("\n3. Cuentas por moneda:")
    print("-" * 80)
    
    try:
        for moneda in ['VES', 'USD', 'EUR', 'USDT']:
            count = db(db.cuentas.moneda == moneda).count()
            print(f"   {moneda}: {count} cuentas")
        
        # Cuentas sin moneda asignada
        sin_moneda = db((db.cuentas.moneda == None) | (db.cuentas.moneda == '')).count()
        print(f"   Sin moneda: {sin_moneda} cuentas")
    except Exception as e:
        print(f"   Error al consultar por moneda: {str(e)}")
    
    # Verificar si hay cuentas con saldos en campos antiguos
    print("\n4. Verificar campos antiguos (saldo_ves, saldo_usd, etc.):")
    print("-" * 80)
    
    try:
        cuentas_con_saldo_ves = db(db.cuentas.saldo_ves > 0).count()
        cuentas_con_saldo_usd = db(db.cuentas.saldo_usd > 0).count()
        cuentas_con_saldo_eur = db(db.cuentas.saldo_eur > 0).count()
        cuentas_con_saldo_usdt = db(db.cuentas.saldo_usdt > 0).count()
        
        print(f"   Cuentas con saldo_ves > 0: {cuentas_con_saldo_ves}")
        print(f"   Cuentas con saldo_usd > 0: {cuentas_con_saldo_usd}")
        print(f"   Cuentas con saldo_eur > 0: {cuentas_con_saldo_eur}")
        print(f"   Cuentas con saldo_usdt > 0: {cuentas_con_saldo_usdt}")
    except Exception as e:
        print(f"   Error al consultar campos antiguos: {str(e)}")
    
    # Verificar si hay cuentas con el nuevo campo 'saldo'
    print("\n5. Verificar nuevo campo 'saldo':")
    print("-" * 80)
    
    try:
        cuentas_con_saldo = db(db.cuentas.saldo > 0).count()
        print(f"   Cuentas con saldo > 0: {cuentas_con_saldo}")
        
        # Calcular saldo total por moneda
        from decimal import Decimal
        print("\n   Saldos totales por moneda:")
        for moneda in ['VES', 'USD', 'EUR', 'USDT']:
            cuentas = db(db.cuentas.moneda == moneda).select()
            total = sum([Decimal(str(c.saldo or 0)) for c in cuentas])
            print(f"      {moneda}: {total:,.4f}")
    except Exception as e:
        print(f"   Error al consultar campo saldo: {str(e)}")
    
    # Verificar clientes
    print("\n6. Información de clientes:")
    print("-" * 80)
    
    total_clientes = db(db.clientes.id > 0).count()
    print(f"   Total de clientes: {total_clientes}")
    
    # Verificar transacciones
    print("\n7. Información de transacciones:")
    print("-" * 80)
    
    total_transacciones = db(db.transacciones.id > 0).count()
    print(f"   Total de transacciones: {total_transacciones}")
    
    try:
        trans_con_cuentas = db(
            (db.transacciones.cuenta_origen_id != None) &
            (db.transacciones.cuenta_destino_id != None)
        ).count()
        print(f"   Transacciones con cuenta_origen_id y cuenta_destino_id: {trans_con_cuentas}")
    except Exception as e:
        print(f"   Error al consultar transacciones: {str(e)}")
    
    print("\n" + "=" * 80)
    print("CONCLUSIÓN")
    print("=" * 80)
    
    # Determinar el estado de la migración
    try:
        cuentas_migradas = db(
            (db.cuentas.moneda != None) &
            (db.cuentas.moneda != '')
        ).count()
        
        if cuentas_migradas > 0:
            print("\n✅ La migración YA HA SIDO EJECUTADA")
            print(f"   Se encontraron {cuentas_migradas} cuentas con moneda asignada")
            print("\n   El sistema ya está usando el nuevo modelo de cuentas por moneda.")
        else:
            print("\n⚠️  La migración NO ha sido ejecutada")
            print("   No se encontraron cuentas con moneda asignada")
    except Exception as e:
        print(f"\n⚠️  No se pudo determinar el estado: {str(e)}")
    
    print("\n" + "=" * 80)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
