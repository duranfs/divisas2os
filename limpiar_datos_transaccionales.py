#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpiar datos transaccionales del sistema de divisas
Limpia: saldos, transacciones, movimientos, remesas y límites
Mantiene: clientes, cuentas (estructura), usuarios

ADVERTENCIA: Este script eliminará TODOS los datos transaccionales
Usar solo en desarrollo o con backup de la base de datos

Uso:
    python web2py.py -S divisas2os_multiple -M -R limpiar_datos_transaccionales.py
"""

from __future__ import print_function
import sys

def confirmar_accion():
    """Solicita confirmación del usuario antes de proceder"""
    print("\n" + "="*70)
    print("ADVERTENCIA: LIMPIEZA DE DATOS TRANSACCIONALES")
    print("="*70)
    print("\nEste script eliminara:")
    print("  X Todas las transacciones")
    print("  X Todos los movimientos")
    print("  X Todas las remesas")
    print("  X Todos los limites de transacciones")
    print("  X Resetear todos los saldos de cuentas a 0.00")
    print("\nSe mantendran:")
    print("  + Clientes")
    print("  + Cuentas (estructura)")
    print("  + Usuarios")
    print("  + Tasas de cambio")
    print("  + Configuracion del sistema")
    print("\n" + "="*70)
    
    try:
        respuesta = raw_input("\nEsta seguro que desea continuar? (escriba 'SI' para confirmar): ")
    except NameError:
        respuesta = input("\nEsta seguro que desea continuar? (escriba 'SI' para confirmar): ")
    return respuesta.strip().upper() == 'SI'

def limpiar_datos():
    """Limpia todos los datos transaccionales del sistema"""
    
    if not confirmar_accion():
        print("\n[X] Operacion cancelada por el usuario")
        return False
    
    print("\nIniciando limpieza de datos transaccionales...")
    print("="*70)
    
    try:
        # Contador de registros eliminados
        contadores = {
            'transacciones': 0,
            'movimientos': 0,
            'remesas': 0,
            'limites': 0,
            'cuentas_actualizadas': 0
        }
        
        # 1. Limpiar transacciones
        print("\n[1] Limpiando transacciones...")
        contadores['transacciones'] = db(db.transacciones.id > 0).count()
        db(db.transacciones.id > 0).delete()
        print("   [OK] %d transacciones eliminadas" % contadores['transacciones'])
        
        # 2. Limpiar movimientos (si existe la tabla)
        if 'movimientos' in db.tables:
            print("\n[2] Limpiando movimientos...")
            contadores['movimientos'] = db(db.movimientos.id > 0).count()
            db(db.movimientos.id > 0).delete()
            print("   [OK] %d movimientos eliminados" % contadores['movimientos'])
        else:
            print("\n[2] Tabla 'movimientos' no existe - omitiendo")
        
        # 3. Limpiar remesas (si existe la tabla)
        if 'remesas' in db.tables:
            print("\n[3] Limpiando remesas...")
            contadores['remesas'] = db(db.remesas.id > 0).count()
            db(db.remesas.id > 0).delete()
            print("   [OK] %d remesas eliminadas" % contadores['remesas'])
        else:
            print("\n[3] Tabla 'remesas' no existe - omitiendo")
        
        # 4. Limpiar limites de transacciones (si existe la tabla)
        if 'limites_transacciones' in db.tables:
            print("\n[4] Limpiando limites de transacciones...")
            contadores['limites'] = db(db.limites_transacciones.id > 0).count()
            db(db.limites_transacciones.id > 0).delete()
            print("   [OK] %d limites eliminados" % contadores['limites'])
        else:
            print("\n[4] Tabla 'limites_transacciones' no existe - omitiendo")
        
        # 5. Resetear saldos de todas las cuentas a 0.00
        print("\n[5] Reseteando saldos de cuentas...")
        cuentas = db(db.cuentas.id > 0).select()
        for cuenta in cuentas:
            # Resetear saldo del nuevo modelo
            if hasattr(cuenta, 'saldo'):
                cuenta.update_record(saldo=0.00)
            
            # Resetear saldos del modelo antiguo (si existen)
            if hasattr(cuenta, 'saldo_ves'):
                cuenta.update_record(
                    saldo_ves=0.00,
                    saldo_usd=0.00,
                    saldo_eur=0.00,
                    saldo_usdt=0.00
                )
            
            contadores['cuentas_actualizadas'] += 1
        
        print("   [OK] %d cuentas reseteadas a saldo 0.00" % contadores['cuentas_actualizadas'])
        
        # 6. Commit de todos los cambios
        db.commit()
        
        # Resumen final
        print("\n" + "="*70)
        print("[OK] LIMPIEZA COMPLETADA EXITOSAMENTE")
        print("="*70)
        print("\nResumen de operaciones:")
        print("   - Transacciones eliminadas: %d" % contadores['transacciones'])
        print("   - Movimientos eliminados: %d" % contadores['movimientos'])
        print("   - Remesas eliminadas: %d" % contadores['remesas'])
        print("   - Limites eliminados: %d" % contadores['limites'])
        print("   - Cuentas reseteadas: %d" % contadores['cuentas_actualizadas'])
        
        print("\n[OK] Base de datos limpia y lista para nuevas transacciones")
        print("="*70)
        
        return True
        
    except Exception as e:
        print("\n[ERROR] durante la limpieza: %s" % str(e))
        db.rollback()
        print("   [!] Se ha revertido la transaccion (rollback)")
        return False

def verificar_estado_post_limpieza():
    """Verifica el estado de la base de datos despues de la limpieza"""
    print("\nVerificando estado de la base de datos...")
    print("="*70)
    
    # Contar registros restantes
    total_clientes = db(db.clientes.id > 0).count()
    total_cuentas = db(db.cuentas.id > 0).count()
    total_usuarios = db(db.auth_user.id > 0).count()
    total_transacciones = db(db.transacciones.id > 0).count()
    
    print("\nEstado actual:")
    print("   - Clientes: %d" % total_clientes)
    print("   - Cuentas: %d" % total_cuentas)
    print("   - Usuarios: %d" % total_usuarios)
    print("   - Transacciones: %d" % total_transacciones)
    
    # Verificar saldos
    cuentas_con_saldo = 0
    try:
        cuentas_con_saldo = db(db.cuentas.saldo > 0).count()
    except:
        pass
    
    print("   - Cuentas con saldo > 0: %d" % cuentas_con_saldo)
    
    if total_transacciones == 0 and cuentas_con_saldo == 0:
        print("\n[OK] Verificacion exitosa: Base de datos limpia")
    else:
        print("\n[!] Advertencia: Aun hay datos transaccionales")
    
    print("="*70)

# Ejecutar el script
print("\n" + "="*70)
print("SCRIPT DE LIMPIEZA DE DATOS TRANSACCIONALES")
print("   Sistema de Divisas Bancario")
print("="*70)

# Ejecutar limpieza
exito = limpiar_datos()

if exito:
    # Verificar estado
    verificar_estado_post_limpieza()
    print("\n[OK] Proceso completado exitosamente\n")
else:
    print("\n[ERROR] Proceso terminado con errores\n")
