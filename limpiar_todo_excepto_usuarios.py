#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpieza COMPLETA del sistema de divisas
Limpia: clientes, cuentas, transacciones, movimientos, remesas, limites
Mantiene: usuarios, tasas de cambio, configuracion

ADVERTENCIA: Este script eliminara TODOS los datos excepto usuarios
Usar solo en desarrollo o con backup de la base de datos

Uso:
    python web2py.py -S divisas2os_multiple -M -R limpiar_todo_excepto_usuarios.py
"""

from __future__ import print_function
import sys

def confirmar_accion():
    """Solicita confirmacion del usuario antes de proceder"""
    print("\n" + "="*70)
    print("ADVERTENCIA: LIMPIEZA COMPLETA DEL SISTEMA")
    print("="*70)
    print("\nEste script eliminara:")
    print("  X Todos los clientes")
    print("  X Todas las cuentas")
    print("  X Todas las transacciones")
    print("  X Todos los movimientos")
    print("  X Todas las remesas")
    print("  X Todos los limites")
    print("\nSe mantendran:")
    print("  + Usuarios (auth_user)")
    print("  + Tasas de cambio")
    print("  + Configuracion del sistema")
    print("  + Logs de auditoria")
    print("\n" + "="*70)
    
    try:
        respuesta = raw_input("\nEsta seguro que desea continuar? (escriba 'ELIMINAR TODO' para confirmar): ")
    except NameError:
        respuesta = input("\nEsta seguro que desea continuar? (escriba 'ELIMINAR TODO' para confirmar): ")
    return respuesta.strip().upper() == 'ELIMINAR TODO'

def limpiar_todo():
    """Limpia todos los datos excepto usuarios y configuración"""
    
    if not confirmar_accion():
        print("\n❌ Operación cancelada por el usuario")
        return False
    
    print("\n🔄 Iniciando limpieza completa del sistema...")
    print("="*70)
    
    try:
        # Contador de registros eliminados
        contadores = {
            'transacciones': 0,
            'movimientos': 0,
            'remesas': 0,
            'limites': 0,
            'cuentas': 0,
            'clientes': 0
        }
        
        # 1. Limpiar transacciones
        print("\n1️⃣  Limpiando transacciones...")
        contadores['transacciones'] = db(db.transacciones.id > 0).count()
        db(db.transacciones.id > 0).delete()
        print(f"   ✓ {contadores['transacciones']} transacciones eliminadas")
        
        # 2. Limpiar movimientos (si existe la tabla)
        if 'movimientos' in db.tables:
            print("\n2️⃣  Limpiando movimientos...")
            contadores['movimientos'] = db(db.movimientos.id > 0).count()
            db(db.movimientos.id > 0).delete()
            print(f"   ✓ {contadores['movimientos']} movimientos eliminados")
        else:
            print("\n2️⃣  Tabla 'movimientos' no existe - omitiendo")
        
        # 3. Limpiar remesas (si existe la tabla)
        if 'remesas' in db.tables:
            print("\n3️⃣  Limpiando remesas...")
            contadores['remesas'] = db(db.remesas.id > 0).count()
            db(db.remesas.id > 0).delete()
            print(f"   ✓ {contadores['remesas']} remesas eliminadas")
        else:
            print("\n3️⃣  Tabla 'remesas' no existe - omitiendo")
        
        # 4. Limpiar límites de transacciones (si existe la tabla)
        if 'limites_transacciones' in db.tables:
            print("\n4️⃣  Limpiando límites de transacciones...")
            contadores['limites'] = db(db.limites_transacciones.id > 0).count()
            db(db.limites_transacciones.id > 0).delete()
            print(f"   ✓ {contadores['limites']} límites eliminados")
        else:
            print("\n4️⃣  Tabla 'limites_transacciones' no existe - omitiendo")
        
        # 5. Limpiar cuentas
        print("\n5️⃣  Limpiando cuentas...")
        contadores['cuentas'] = db(db.cuentas.id > 0).count()
        db(db.cuentas.id > 0).delete()
        print(f"   ✓ {contadores['cuentas']} cuentas eliminadas")
        
        # 6. Limpiar clientes
        print("\n6️⃣  Limpiando clientes...")
        contadores['clientes'] = db(db.clientes.id > 0).count()
        db(db.clientes.id > 0).delete()
        print(f"   ✓ {contadores['clientes']} clientes eliminados")
        
        # 7. Commit de todos los cambios
        db.commit()
        
        # Resumen final
        print("\n" + "="*70)
        print("✅ LIMPIEZA COMPLETA EXITOSA")
        print("="*70)
        print("\n📊 Resumen de operaciones:")
        print(f"   • Transacciones eliminadas: {contadores['transacciones']}")
        print(f"   • Movimientos eliminados: {contadores['movimientos']}")
        print(f"   • Remesas eliminadas: {contadores['remesas']}")
        print(f"   • Límites eliminados: {contadores['limites']}")
        print(f"   • Cuentas eliminadas: {contadores['cuentas']}")
        print(f"   • Clientes eliminados: {contadores['clientes']}")
        
        print("\n✓ Sistema limpio y listo para empezar desde cero")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR durante la limpieza: {str(e)}")
        db.rollback()
        print("   ⚠️  Se ha revertido la transacción (rollback)")
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
    total_tasas = db(db.tasas_cambio.id > 0).count()
    
    print(f"\n📈 Estado actual:")
    print(f"   • Clientes: {total_clientes}")
    print(f"   • Cuentas: {total_cuentas}")
    print(f"   • Transacciones: {total_transacciones}")
    print(f"   • Usuarios (mantenidos): {total_usuarios}")
    print(f"   • Tasas de cambio (mantenidas): {total_tasas}")
    
    if total_clientes == 0 and total_cuentas == 0 and total_transacciones == 0:
        print("\n✅ Verificación exitosa: Sistema completamente limpio")
        print("   Puede comenzar a crear nuevos clientes y cuentas")
    else:
        print("\n⚠️  Advertencia: Aún hay datos en el sistema")
    
    print("="*70)

# Ejecutar el script
if __name__ == '__main__':
    print("\n" + "="*70)
    print("🧹 SCRIPT DE LIMPIEZA COMPLETA DEL SISTEMA")
    print("   Sistema de Divisas Bancario")
    print("="*70)
    
    # Ejecutar limpieza
    exito = limpiar_todo()
    
    if exito:
        # Verificar estado
        verificar_estado_post_limpieza()
        print("\n✅ Proceso completado exitosamente\n")
        sys.exit(0)
    else:
        print("\n❌ Proceso terminado con errores\n")
        sys.exit(1)
