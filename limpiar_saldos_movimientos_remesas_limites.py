#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpiar saldos, movimientos, remesas y límites del sistema
Limpia: saldos de cuentas, movimientos, remesas, límites
Mantiene: clientes, cuentas (estructura), usuarios, transacciones, tasas

ADVERTENCIA: Este script eliminará datos específicos de operaciones
Usar solo en desarrollo o con backup de la base de datos

Uso:
    python web2py.py -S divisas2os_multiple -M -R limpiar_saldos_movimientos_remesas_limites.py
"""

from __future__ import print_function
import sys

def confirmar_accion():
    """Solicita confirmación del usuario antes de proceder"""
    print("\n" + "="*70)
    print("ADVERTENCIA: LIMPIEZA DE SALDOS, MOVIMIENTOS, REMESAS Y LIMITES")
    print("="*70)
    print("\nEste script eliminara:")
    print("  X Todos los movimientos de cuenta")
    print("  X Todas las remesas diarias")
    print("  X Todos los movimientos de remesas")
    print("  X Todos los limites de venta")
    print("  X Todas las alertas de limites")
    print("  X Resetear todos los saldos de cuentas a 0.00")
    print("\nSe mantendran:")
    print("  + Clientes")
    print("  + Cuentas (estructura)")
    print("  + Usuarios")
    print("  + Transacciones")
    print("  + Tasas de cambio")
    print("  + Configuracion del sistema")
    print("\n" + "="*70)
    
    try:
        respuesta = raw_input("\nEsta seguro que desea continuar? (escriba 'SI' para confirmar): ")
    except NameError:
        respuesta = input("\nEsta seguro que desea continuar? (escriba 'SI' para confirmar): ")
    return respuesta.strip().upper() == 'SI'

def limpiar_datos():
    """Limpia saldos, movimientos, remesas y límites del sistema"""
    
    if not confirmar_accion():
        print("\n❌ Operacion cancelada por el usuario")
        return False
    
    print("\n🔄 Iniciando limpieza de saldos, movimientos, remesas y limites...")
    print("="*70)
    
    try:
        # Contador de registros eliminados
        contadores = {
            'movimientos_cuenta': 0,
            'remesas_diarias': 0,
            'movimientos_remesas': 0,
            'limites_venta': 0,
            'alertas_limites': 0,
            'cuentas_reseteadas': 0
        }
        
        # 1. Limpiar movimientos de cuenta
        if 'movimientos_cuenta' in db.tables:
            print("\n1️⃣  Limpiando movimientos de cuenta...")
            contadores['movimientos_cuenta'] = db(db.movimientos_cuenta.id > 0).count()
            db(db.movimientos_cuenta.id > 0).delete()
            print(f"   ✓ {contadores['movimientos_cuenta']} movimientos de cuenta eliminados")
        else:
            print("\n1️⃣  Tabla 'movimientos_cuenta' no existe - omitiendo")
        
        # 2. Limpiar movimientos de remesas
        if 'movimientos_remesas' in db.tables:
            print("\n2️⃣  Limpiando movimientos de remesas...")
            contadores['movimientos_remesas'] = db(db.movimientos_remesas.id > 0).count()
            db(db.movimientos_remesas.id > 0).delete()
            print(f"   ✓ {contadores['movimientos_remesas']} movimientos de remesas eliminados")
        else:
            print("\n2️⃣  Tabla 'movimientos_remesas' no existe - omitiendo")
        
        # 3. Limpiar remesas diarias
        if 'remesas_diarias' in db.tables:
            print("\n3️⃣  Limpiando remesas diarias...")
            contadores['remesas_diarias'] = db(db.remesas_diarias.id > 0).count()
            db(db.remesas_diarias.id > 0).delete()
            print(f"   ✓ {contadores['remesas_diarias']} remesas diarias eliminadas")
        else:
            print("\n3️⃣  Tabla 'remesas_diarias' no existe - omitiendo")
        
        # 4. Limpiar límites de venta
        if 'limites_venta' in db.tables:
            print("\n4️⃣  Limpiando limites de venta...")
            contadores['limites_venta'] = db(db.limites_venta.id > 0).count()
            db(db.limites_venta.id > 0).delete()
            print(f"   ✓ {contadores['limites_venta']} limites de venta eliminados")
        else:
            print("\n4️⃣  Tabla 'limites_venta' no existe - omitiendo")
        
        # 5. Limpiar alertas de límites
        if 'alertas_limites' in db.tables:
            print("\n5️⃣  Limpiando alertas de limites...")
            contadores['alertas_limites'] = db(db.alertas_limites.id > 0).count()
            db(db.alertas_limites.id > 0).delete()
            print(f"   ✓ {contadores['alertas_limites']} alertas de limites eliminadas")
        else:
            print("\n5️⃣  Tabla 'alertas_limites' no existe - omitiendo")
        
        # 6. Resetear saldos de todas las cuentas a 0.00
        print("\n6️⃣  Reseteando saldos de cuentas...")
        cuentas = db(db.cuentas.id > 0).select()
        for cuenta in cuentas:
            # Resetear saldo del nuevo modelo (cuenta por moneda)
            if hasattr(cuenta, 'saldo'):
                cuenta.update_record(saldo=0.00)
            
            # Resetear saldos del modelo antiguo (si existen)
            if hasattr(cuenta, 'saldo_ves'):
                cuenta.update_record(
                    saldo_ves=0.00,
                    saldo_usd=0.00,
                    saldo_eur=0.00
                )
            
            # Resetear USDT si existe
            if hasattr(cuenta, 'saldo_usdt'):
                cuenta.update_record(saldo_usdt=0.00)
            
            contadores['cuentas_reseteadas'] += 1
        
        print(f"   ✓ {contadores['cuentas_reseteadas']} cuentas reseteadas a saldo 0.00")
        
        # 7. Commit de todos los cambios
        db.commit()
        
        # Resumen final
        print("\n" + "="*70)
        print("✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
        print("="*70)
        print("\n📊 Resumen de operaciones:")
        print(f"   • Movimientos de cuenta eliminados: {contadores['movimientos_cuenta']}")
        print(f"   • Movimientos de remesas eliminados: {contadores['movimientos_remesas']}")
        print(f"   • Remesas diarias eliminadas: {contadores['remesas_diarias']}")
        print(f"   • Limites de venta eliminados: {contadores['limites_venta']}")
        print(f"   • Alertas de limites eliminadas: {contadores['alertas_limites']}")
        print(f"   • Cuentas reseteadas: {contadores['cuentas_reseteadas']}")
        
        print("\n✓ Sistema limpio y listo para nuevas operaciones")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR durante la limpieza: {str(e)}")
        db.rollback()
        print("   ⚠️  Se ha revertido la transaccion (rollback)")
        import traceback
        traceback.print_exc()
        return False

def verificar_estado_post_limpieza():
    """Verifica el estado de la base de datos después de la limpieza"""
    print("\n🔍 Verificando estado de la base de datos...")
    print("="*70)
    
    # Contar registros restantes
    total_clientes = db(db.clientes.id > 0).count()
    total_cuentas = db(db.cuentas.id > 0).count()
    total_usuarios = db(db.auth_user.id > 0).count()
    total_transacciones = db(db.transacciones.id > 0).count()
    
    print(f"\n📈 Estado actual:")
    print(f"   • Clientes (mantenidos): {total_clientes}")
    print(f"   • Cuentas (mantenidas): {total_cuentas}")
    print(f"   • Usuarios (mantenidos): {total_usuarios}")
    print(f"   • Transacciones (mantenidas): {total_transacciones}")
    
    # Verificar tablas limpiadas
    if 'movimientos_cuenta' in db.tables:
        total_movimientos = db(db.movimientos_cuenta.id > 0).count()
        print(f"   • Movimientos de cuenta: {total_movimientos}")
    
    if 'remesas_diarias' in db.tables:
        total_remesas = db(db.remesas_diarias.id > 0).count()
        print(f"   • Remesas diarias: {total_remesas}")
    
    if 'movimientos_remesas' in db.tables:
        total_mov_remesas = db(db.movimientos_remesas.id > 0).count()
        print(f"   • Movimientos de remesas: {total_mov_remesas}")
    
    if 'limites_venta' in db.tables:
        total_limites = db(db.limites_venta.id > 0).count()
        print(f"   • Limites de venta: {total_limites}")
    
    if 'alertas_limites' in db.tables:
        total_alertas = db(db.alertas_limites.id > 0).count()
        print(f"   • Alertas de limites: {total_alertas}")
    
    # Verificar saldos
    cuentas_con_saldo = 0
    try:
        if 'saldo' in db.cuentas.fields:
            cuentas_con_saldo = db(db.cuentas.saldo > 0).count()
        elif 'saldo_ves' in db.cuentas.fields:
            cuentas_con_saldo = db(
                (db.cuentas.saldo_ves > 0) | 
                (db.cuentas.saldo_usd > 0) | 
                (db.cuentas.saldo_eur > 0)
            ).count()
    except:
        pass
    
    print(f"   • Cuentas con saldo > 0: {cuentas_con_saldo}")
    
    # Verificación final
    tablas_vacias = True
    if 'movimientos_cuenta' in db.tables:
        tablas_vacias = tablas_vacias and (db(db.movimientos_cuenta.id > 0).count() == 0)
    if 'remesas_diarias' in db.tables:
        tablas_vacias = tablas_vacias and (db(db.remesas_diarias.id > 0).count() == 0)
    if 'movimientos_remesas' in db.tables:
        tablas_vacias = tablas_vacias and (db(db.movimientos_remesas.id > 0).count() == 0)
    if 'limites_venta' in db.tables:
        tablas_vacias = tablas_vacias and (db(db.limites_venta.id > 0).count() == 0)
    if 'alertas_limites' in db.tables:
        tablas_vacias = tablas_vacias and (db(db.alertas_limites.id > 0).count() == 0)
    
    if tablas_vacias and cuentas_con_saldo == 0:
        print("\n✅ Verificacion exitosa: Saldos, movimientos, remesas y limites limpiados")
        print("   Puede comenzar a registrar nuevas operaciones")
    else:
        print("\n⚠️  Advertencia: Aun hay datos en algunas tablas")
    
    print("="*70)

# Ejecutar el script
if __name__ == '__main__':
    print("\n" + "="*70)
    print("🧹 SCRIPT DE LIMPIEZA DE SALDOS, MOVIMIENTOS, REMESAS Y LIMITES")
    print("   Sistema de Divisas Bancario")
    print("="*70)
    
    # Ejecutar limpieza
    exito = limpiar_datos()
    
    if exito:
        # Verificar estado
        verificar_estado_post_limpieza()
        print("\n✅ Proceso completado exitosamente\n")
        sys.exit(0)
    else:
        print("\n❌ Proceso terminado con errores\n")
        sys.exit(1)
