# -*- coding: utf-8 -*-
"""
Script de Verificación Pre-Migración
Sistema de Divisas Bancario

Este script verifica el estado actual del sistema antes de ejecutar la migración.

Uso:
    python web2py.py -S sistema_divisas -M -R verificar_estado_pre_migracion.py

Autor: Sistema de Divisas Bancario
Fecha: 2025-11-25
"""

from decimal import Decimal
import datetime

def verificar_estado_pre_migracion():
    """Verifica el estado actual del sistema antes de la migración"""
    
    print("\n" + "=" * 80)
    print("VERIFICACIÓN PRE-MIGRACIÓN")
    print("Sistema de Divisas Bancario")
    print("=" * 80)
    print(f"\nFecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar contexto
    try:
        if 'db' not in globals():
            print("\n❌ Error: Este script debe ejecutarse con web2py")
            return False
        
        if 'cuentas' not in db.tables:
            print("\n❌ Error: La tabla 'cuentas' no existe")
            return False
        
        print("\n✅ Contexto verificado correctamente")
        
    except Exception as e:
        print(f"\n❌ Error al verificar contexto: {str(e)}")
        return False
    
    print("\n" + "-" * 80)
    print("1. ESTADO ACTUAL DE LA BASE DE DATOS")
    print("-" * 80)
    
    # Contar cuentas totales
    total_cuentas = db(db.cuentas.id > 0).count()
    print(f"\n📊 Total de cuentas: {total_cuentas}")
    
    # Verificar si ya hay cuentas migradas
    cuentas_con_moneda = db(
        (db.cuentas.moneda != None) & 
        (db.cuentas.moneda != '') &
        (db.cuentas.moneda != 'VES')
    ).count()
    
    if cuentas_con_moneda > 0:
        print(f"\n⚠️  ADVERTENCIA: Ya hay {cuentas_con_moneda} cuentas con moneda asignada (no VES)")
        print("   Esto sugiere que la migración ya se ejecutó parcialmente")
        
        # Mostrar distribución por moneda
        print("\n   Distribución actual por moneda:")
        for moneda in ['VES', 'USD', 'EUR', 'USDT']:
            count = db(db.cuentas.moneda == moneda).count()
            if count > 0:
                print(f"      {moneda}: {count} cuentas")
        
        respuesta = input("\n¿Desea continuar de todos modos? (SI/NO): ")
        if respuesta.strip().upper() != 'SI':
            print("\n❌ Verificación cancelada por el usuario")
            return False
    else:
        print("\n✅ No se detectaron cuentas migradas previamente")
    
    print("\n" + "-" * 80)
    print("2. ANÁLISIS DE SALDOS ACTUALES")
    print("-" * 80)
    
    # Calcular saldos totales en campos antiguos
    cuentas = db(db.cuentas.id > 0).select()
    
    saldos_totales = {
        'VES': Decimal('0'),
        'USD': Decimal('0'),
        'EUR': Decimal('0'),
        'USDT': Decimal('0')
    }
    
    cuentas_con_saldo = {
        'VES': 0,
        'USD': 0,
        'EUR': 0,
        'USDT': 0
    }
    
    for cuenta in cuentas:
        saldo_ves = Decimal(str(cuenta.saldo_ves or 0))
        saldo_usd = Decimal(str(cuenta.saldo_usd or 0))
        saldo_eur = Decimal(str(cuenta.saldo_eur or 0))
        saldo_usdt = Decimal(str(cuenta.saldo_usdt or 0))
        
        saldos_totales['VES'] += saldo_ves
        saldos_totales['USD'] += saldo_usd
        saldos_totales['EUR'] += saldo_eur
        saldos_totales['USDT'] += saldo_usdt
        
        if saldo_ves > 0:
            cuentas_con_saldo['VES'] += 1
        if saldo_usd > 0:
            cuentas_con_saldo['USD'] += 1
        if saldo_eur > 0:
            cuentas_con_saldo['EUR'] += 1
        if saldo_usdt > 0:
            cuentas_con_saldo['USDT'] += 1
    
    print("\n💰 Saldos totales en campos antiguos:")
    for moneda, saldo in saldos_totales.items():
        print(f"   {moneda}: {saldo:,.4f}")
    
    print("\n📈 Cuentas con saldo > 0 por moneda:")
    for moneda, count in cuentas_con_saldo.items():
        print(f"   {moneda}: {count} cuentas")
    
    # Estimar cuentas que se crearán
    cuentas_a_crear = sum(cuentas_con_saldo.values())
    # Agregar cuentas VES para clientes sin saldo VES
    cuentas_sin_ves = total_cuentas - cuentas_con_saldo['VES']
    cuentas_a_crear += cuentas_sin_ves
    
    print(f"\n📊 Estimación de cuentas a crear: {cuentas_a_crear}")
    print(f"   (Total actual: {total_cuentas} → Después: ~{cuentas_a_crear})")
    
    print("\n" + "-" * 80)
    print("3. VERIFICACIÓN DE CLIENTES")
    print("-" * 80)
    
    total_clientes = db(db.clientes.id > 0).count()
    print(f"\n📊 Total de clientes: {total_clientes}")
    
    # Verificar clientes con cuentas
    clientes_con_cuentas = db(db.cuentas.id > 0).select(
        db.cuentas.cliente_id,
        distinct=True
    )
    
    print(f"✅ Clientes con cuentas: {len(clientes_con_cuentas)}")
    
    if len(clientes_con_cuentas) < total_clientes:
        clientes_sin_cuentas = total_clientes - len(clientes_con_cuentas)
        print(f"⚠️  Clientes sin cuentas: {clientes_sin_cuentas}")
    
    print("\n" + "-" * 80)
    print("4. VERIFICACIÓN DE TRANSACCIONES")
    print("-" * 80)
    
    total_transacciones = db(db.transacciones.id > 0).count()
    print(f"\n📊 Total de transacciones: {total_transacciones}")
    
    # Verificar transacciones con nuevos campos
    transacciones_nuevas = db(
        (db.transacciones.cuenta_origen_id != None) &
        (db.transacciones.cuenta_destino_id != None)
    ).count()
    
    transacciones_antiguas = total_transacciones - transacciones_nuevas
    
    print(f"✅ Transacciones con nuevo modelo: {transacciones_nuevas}")
    print(f"⚠️  Transacciones con modelo antiguo: {transacciones_antiguas}")
    
    print("\n" + "-" * 80)
    print("5. VERIFICACIÓN DE BACKUPS")
    print("-" * 80)
    
    import os
    
    backup_dir = os.path.join(request.folder, 'backups')
    
    if os.path.exists(backup_dir):
        backups = [f for f in os.listdir(backup_dir) if f.endswith('.sqlite')]
        backups.sort(reverse=True)
        
        print(f"\n📁 Backups disponibles: {len(backups)}")
        
        if backups:
            print("\n   Últimos 3 backups:")
            for backup in backups[:3]:
                backup_path = os.path.join(backup_dir, backup)
                size = os.path.getsize(backup_path) / (1024 * 1024)
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(backup_path))
                print(f"      - {backup}")
                print(f"        Tamaño: {size:.2f} MB | Fecha: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("\n⚠️  No hay backups disponibles")
            print("   Se recomienda crear un backup manual antes de continuar")
    else:
        print("\n⚠️  Directorio de backups no existe")
        print("   Se creará automáticamente durante la migración")
    
    print("\n" + "=" * 80)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 80)
    
    print(f"\n✅ Sistema listo para migración")
    print(f"\n📊 Estadísticas:")
    print(f"   - Cuentas actuales: {total_cuentas}")
    print(f"   - Cuentas estimadas después: ~{cuentas_a_crear}")
    print(f"   - Clientes: {total_clientes}")
    print(f"   - Transacciones: {total_transacciones}")
    
    print(f"\n💰 Saldos a migrar:")
    for moneda, saldo in saldos_totales.items():
        if saldo > 0:
            print(f"   - {moneda}: {saldo:,.4f} ({cuentas_con_saldo[moneda]} cuentas)")
    
    print("\n" + "=" * 80)
    print("RECOMENDACIONES")
    print("=" * 80)
    
    print("\n1. ✅ Asegúrese de tener un backup reciente")
    print("2. ✅ Detenga el servidor web si está en producción")
    print("3. ✅ Verifique que no haya usuarios conectados")
    print("4. ✅ Revise el espacio en disco disponible")
    print("5. ✅ Tenga a mano el plan de reversión")
    
    print("\n" + "=" * 80)
    print("¿LISTO PARA CONTINUAR?")
    print("=" * 80)
    
    print("\nPara ejecutar la migración, use:")
    print("   python web2py.py -S sistema_divisas -M -R ejecutar_migracion_produccion.py")
    
    print("\nO ejecute el archivo batch:")
    print("   EJECUTAR_MIGRACION_FINAL.bat")
    
    print("\n" + "=" * 80)
    
    return True

# Ejecutar verificación
if __name__ == '__main__':
    try:
        verificar_estado_pre_migracion()
    except Exception as e:
        print(f"\n❌ ERROR durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
