# -*- coding: utf-8 -*-
"""
Script de Ejecución de Migración en Producción
Sistema de Divisas Bancario

Este script ejecuta la migración completa de cuentas multi-moneda a cuentas individuales
por moneda, incluyendo backup, migración, validación y verificación.

Uso:
    python web2py.py -S sistema_divisas -M -R ejecutar_migracion_produccion.py

Autor: Sistema de Divisas Bancario
Fecha: 2025-11-25
"""

import sys
import os
import shutil
import datetime
from decimal import Decimal

# -------------------------------------------------------------------------
# PASO 1: BACKUP COMPLETO DE LA BASE DE DATOS
# -------------------------------------------------------------------------

def realizar_backup_completo():
    """
    Realiza un backup completo de la base de datos antes de la migración
    
    Returns:
        Tuple (bool, str) - (exitoso, ruta_backup)
    """
    print("\n" + "=" * 80)
    print("PASO 1: BACKUP COMPLETO DE LA BASE DE DATOS")
    print("=" * 80)
    
    try:
        # Determinar rutas
        app_path = os.path.join(request.folder)
        db_path = os.path.join(app_path, 'databases', 'storage.sqlite')
        backup_dir = os.path.join(app_path, 'backups')
        
        # Crear directorio de backups si no existe
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            print(f"✅ Directorio de backups creado: {backup_dir}")
        
        # Verificar que existe la BD
        if not os.path.exists(db_path):
            print(f"❌ ERROR: No se encontró la base de datos en: {db_path}")
            return False, None
        
        # Obtener información de la BD
        db_size = os.path.getsize(db_path)
        db_size_mb = db_size / (1024 * 1024)
        
        print(f"\n📊 Información de la base de datos:")
        print(f"   Ubicación: {db_path}")
        print(f"   Tamaño: {db_size_mb:.2f} MB")
        
        # Nombre del backup con timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'storage_antes_migracion_produccion_{timestamp}.sqlite'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Realizar backup
        print(f"\n🔄 Realizando backup...")
        shutil.copy2(db_path, backup_path)
        
        # Verificar backup
        if os.path.exists(backup_path):
            backup_size = os.path.getsize(backup_path)
            if backup_size == db_size:
                print(f"✅ Backup completado exitosamente!")
                print(f"\n📁 Backup guardado en:")
                print(f"   {backup_path}")
                print(f"   Tamaño: {backup_size / (1024 * 1024):.2f} MB")
                
                # Listar backups recientes
                print(f"\n📋 Backups recientes:")
                backups = [f for f in os.listdir(backup_dir) if f.endswith('.sqlite')]
                backups.sort(reverse=True)
                
                for backup in backups[:3]:
                    backup_full_path = os.path.join(backup_dir, backup)
                    size = os.path.getsize(backup_full_path) / (1024 * 1024)
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(backup_full_path))
                    print(f"   - {backup} ({size:.2f} MB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
                
                return True, backup_path
            else:
                print(f"⚠️  Advertencia: El tamaño del backup no coincide")
                print(f"   Original: {db_size_mb:.2f} MB")
                print(f"   Backup: {backup_size / (1024 * 1024):.2f} MB")
                return False, None
        else:
            print(f"❌ ERROR: No se pudo crear el backup")
            return False, None
            
    except Exception as e:
        print(f"\n❌ ERROR durante el backup: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

# -------------------------------------------------------------------------
# PASO 2: EJECUTAR SCRIPT DE MIGRACIÓN
# -------------------------------------------------------------------------

def ejecutar_migracion():
    """
    Ejecuta el script de migración migrar_cuentas.py
    
    Returns:
        Dict con estadísticas de la migración o None si falla
    """
    print("\n" + "=" * 80)
    print("PASO 2: EJECUTAR SCRIPT DE MIGRACIÓN")
    print("=" * 80)
    
    try:
        # Importar funciones del script de migración
        import random
        
        # Función de generación de números de cuenta
        def generar_numero_cuenta_por_moneda(moneda):
            prefijos = {
                'VES': '01',
                'USD': '02',
                'EUR': '03',
                'USDT': '04'
            }
            
            prefijo = prefijos.get(moneda, '01')
            max_intentos = 100
            
            for intento in range(max_intentos):
                digitos = ''.join([str(random.randint(0, 9)) for _ in range(18)])
                numero_cuenta = prefijo + digitos
                
                if db(db.cuentas.numero_cuenta == numero_cuenta).count() == 0:
                    return numero_cuenta
            
            raise Exception(f"No se pudo generar número de cuenta único para moneda {moneda}")
        
        # Función de migración
        print("\n🔄 Iniciando migración de cuentas...")
        
        # Obtener todas las cuentas actuales
        cuentas_antiguas = db(db.cuentas.id > 0).select()
        total_cuentas = len(cuentas_antiguas)
        
        print(f"\n📊 Total de cuentas a procesar: {total_cuentas}")
        
        # Estadísticas
        stats = {
            'cuentas_procesadas': 0,
            'cuentas_creadas': 0,
            'cuentas_con_ves': 0,
            'cuentas_con_usd': 0,
            'cuentas_con_eur': 0,
            'cuentas_con_usdt': 0,
            'errores': [],
            'saldo_total_antes': {
                'VES': Decimal('0'),
                'USD': Decimal('0'),
                'EUR': Decimal('0'),
                'USDT': Decimal('0')
            },
            'saldo_total_despues': {
                'VES': Decimal('0'),
                'USD': Decimal('0'),
                'EUR': Decimal('0'),
                'USDT': Decimal('0')
            }
        }
        
        # Calcular saldos totales antes
        for cuenta in cuentas_antiguas:
            stats['saldo_total_antes']['VES'] += Decimal(str(cuenta.saldo_ves or 0))
            stats['saldo_total_antes']['USD'] += Decimal(str(cuenta.saldo_usd or 0))
            stats['saldo_total_antes']['EUR'] += Decimal(str(cuenta.saldo_eur or 0))
            stats['saldo_total_antes']['USDT'] += Decimal(str(cuenta.saldo_usdt or 0))
        
        print("\n💰 Saldos totales ANTES de la migración:")
        for moneda, saldo in stats['saldo_total_antes'].items():
            print(f"   {moneda}: {saldo:,.4f}")
        
        print("\n" + "-" * 80)
        print("Procesando cuentas...")
        print("-" * 80)
        
        # Procesar cada cuenta
        for idx, cuenta_antigua in enumerate(cuentas_antiguas, 1):
            try:
                cliente_id = cuenta_antigua.cliente_id
                
                if idx % 10 == 0 or idx == 1:
                    print(f"\n[{idx}/{total_cuentas}] Procesando cuenta {cuenta_antigua.numero_cuenta}")
                
                # Obtener saldos
                monedas_saldos = {
                    'VES': Decimal(str(cuenta_antigua.saldo_ves or 0)),
                    'USD': Decimal(str(cuenta_antigua.saldo_usd or 0)),
                    'EUR': Decimal(str(cuenta_antigua.saldo_eur or 0)),
                    'USDT': Decimal(str(cuenta_antigua.saldo_usdt or 0))
                }
                
                # Procesar cada moneda
                for moneda, saldo in monedas_saldos.items():
                    if saldo > 0 or moneda == 'VES':
                        # Verificar si ya existe
                        cuenta_existente = db(
                            (db.cuentas.cliente_id == cliente_id) &
                            (db.cuentas.moneda == moneda) &
                            (db.cuentas.estado == 'activa')
                        ).select().first()
                        
                        if cuenta_existente:
                            continue
                        
                        # Determinar número de cuenta
                        if moneda == 'VES':
                            numero_cuenta = cuenta_antigua.numero_cuenta
                        else:
                            numero_cuenta = generar_numero_cuenta_por_moneda(moneda)
                        
                        # Crear cuenta
                        try:
                            nuevo_id = db.cuentas.insert(
                                cliente_id=cliente_id,
                                numero_cuenta=numero_cuenta,
                                tipo_cuenta=cuenta_antigua.tipo_cuenta,
                                moneda=moneda,
                                saldo=float(saldo),
                                estado='activa',
                                fecha_creacion=cuenta_antigua.fecha_creacion,
                                saldo_ves=0,
                                saldo_usd=0,
                                saldo_eur=0,
                                saldo_usdt=0
                            )
                            
                            stats['cuentas_creadas'] += 1
                            stats[f'cuentas_con_{moneda.lower()}'] += 1
                            stats['saldo_total_despues'][moneda] += saldo
                            
                        except Exception as insert_error:
                            error_msg = f"Error al crear cuenta {moneda} para cliente {cliente_id}: {str(insert_error)}"
                            stats['errores'].append(error_msg)
                
                stats['cuentas_procesadas'] += 1
                
            except Exception as e:
                error_msg = f"Error al procesar cuenta {cuenta_antigua.numero_cuenta}: {str(e)}"
                stats['errores'].append(error_msg)
        
        # Commit
        db.commit()
        print("\n✅ Migración completada y cambios guardados")
        
        return stats
        
    except Exception as e:
        print(f"\n❌ ERROR durante la migración: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None

# -------------------------------------------------------------------------
# PASO 3: VALIDAR INTEGRIDAD DE DATOS MIGRADOS
# -------------------------------------------------------------------------

def validar_integridad_datos(stats):
    """
    Valida que la migración se haya realizado correctamente
    
    Args:
        stats: Estadísticas de la migración
        
    Returns:
        Tuple (bool, list) - (es_valida, lista_de_problemas)
    """
    print("\n" + "=" * 80)
    print("PASO 3: VALIDAR INTEGRIDAD DE DATOS MIGRADOS")
    print("=" * 80)
    
    problemas = []
    
    # 1. Verificar saldos
    print("\n1. Verificando integridad de saldos...")
    
    for moneda in ['VES', 'USD', 'EUR', 'USDT']:
        saldo_antes = stats['saldo_total_antes'][moneda]
        saldo_despues = stats['saldo_total_despues'][moneda]
        diferencia = abs(saldo_antes - saldo_despues)
        
        if diferencia > Decimal('0.01'):
            problema = f"❌ Diferencia en saldos de {moneda}: Antes={saldo_antes}, Después={saldo_despues}, Diferencia={diferencia}"
            print(f"   {problema}")
            problemas.append(problema)
        else:
            print(f"   ✅ {moneda}: Saldos coinciden (Antes={saldo_antes}, Después={saldo_despues})")
    
    # 2. Verificar cuentas creadas
    print("\n2. Verificando cuentas creadas...")
    print(f"   ✅ Cuentas procesadas: {stats['cuentas_procesadas']}")
    print(f"   ✅ Cuentas creadas: {stats['cuentas_creadas']}")
    print(f"   ✅ Cuentas VES: {stats['cuentas_con_ves']}")
    print(f"   ✅ Cuentas USD: {stats['cuentas_con_usd']}")
    print(f"   ✅ Cuentas EUR: {stats['cuentas_con_eur']}")
    print(f"   ✅ Cuentas USDT: {stats['cuentas_con_usdt']}")
    
    # 3. Verificar errores
    if stats['errores']:
        print(f"\n3. ⚠️  Se encontraron {len(stats['errores'])} errores:")
        for error in stats['errores'][:5]:  # Mostrar primeros 5
            print(f"   - {error}")
            problemas.append(error)
        if len(stats['errores']) > 5:
            print(f"   ... y {len(stats['errores']) - 5} errores más")
    else:
        print("\n3. ✅ No se encontraron errores durante la migración")
    
    es_valida = len(problemas) == 0
    
    return es_valida, problemas

# -------------------------------------------------------------------------
# PASO 4: VERIFICAR QUE TODAS LAS CUENTAS SE CREARON CORRECTAMENTE
# -------------------------------------------------------------------------

def verificar_cuentas_creadas():
    """
    Verifica que todas las cuentas se crearon correctamente en la base de datos
    
    Returns:
        Dict con información de verificación
    """
    print("\n" + "=" * 80)
    print("PASO 4: VERIFICAR QUE TODAS LAS CUENTAS SE CREARON CORRECTAMENTE")
    print("=" * 80)
    
    verificacion = {
        'total_cuentas': 0,
        'cuentas_por_moneda': {},
        'clientes_con_cuentas': 0,
        'cuentas_sin_cliente': 0,
        'numeros_duplicados': [],
        'problemas': []
    }
    
    try:
        # 1. Contar cuentas totales
        total_cuentas = db(db.cuentas.id > 0).count()
        verificacion['total_cuentas'] = total_cuentas
        print(f"\n1. Total de cuentas en la base de datos: {total_cuentas}")
        
        # 2. Contar por moneda
        print("\n2. Cuentas por moneda:")
        for moneda in ['VES', 'USD', 'EUR', 'USDT']:
            count = db(db.cuentas.moneda == moneda).count()
            verificacion['cuentas_por_moneda'][moneda] = count
            print(f"   {moneda}: {count} cuentas")
        
        # 3. Verificar clientes con cuentas
        print("\n3. Verificando clientes...")
        clientes_con_cuentas = db(db.cuentas.id > 0).select(
            db.cuentas.cliente_id,
            distinct=True
        )
        verificacion['clientes_con_cuentas'] = len(clientes_con_cuentas)
        print(f"   ✅ Clientes con cuentas: {len(clientes_con_cuentas)}")
        
        # 4. Verificar cuentas sin cliente
        cuentas_sin_cliente = db(db.cuentas.cliente_id == None).count()
        verificacion['cuentas_sin_cliente'] = cuentas_sin_cliente
        if cuentas_sin_cliente > 0:
            print(f"   ⚠️  Cuentas sin cliente: {cuentas_sin_cliente}")
            verificacion['problemas'].append(f"Hay {cuentas_sin_cliente} cuentas sin cliente")
        else:
            print(f"   ✅ No hay cuentas sin cliente")
        
        # 5. Verificar números de cuenta duplicados
        print("\n4. Verificando números de cuenta duplicados...")
        numeros = db(db.cuentas.id > 0).select(db.cuentas.numero_cuenta)
        numeros_lista = [n.numero_cuenta for n in numeros]
        numeros_unicos = set(numeros_lista)
        
        if len(numeros_lista) != len(numeros_unicos):
            duplicados = [n for n in numeros_unicos if numeros_lista.count(n) > 1]
            verificacion['numeros_duplicados'] = duplicados
            print(f"   ⚠️  Se encontraron {len(duplicados)} números duplicados:")
            for dup in duplicados[:5]:
                print(f"      - {dup}")
            verificacion['problemas'].append(f"Hay {len(duplicados)} números de cuenta duplicados")
        else:
            print(f"   ✅ No hay números de cuenta duplicados")
        
        # 6. Verificar prefijos de números de cuenta
        print("\n5. Verificando prefijos de números de cuenta...")
        prefijos_esperados = {'VES': '01', 'USD': '02', 'EUR': '03', 'USDT': '04'}
        
        for moneda, prefijo in prefijos_esperados.items():
            cuentas_moneda = db(db.cuentas.moneda == moneda).select()
            cuentas_sin_prefijo = [c for c in cuentas_moneda if not c.numero_cuenta.startswith(prefijo)]
            
            if cuentas_sin_prefijo:
                print(f"   ⚠️  {len(cuentas_sin_prefijo)} cuentas {moneda} sin prefijo correcto")
                verificacion['problemas'].append(f"{len(cuentas_sin_prefijo)} cuentas {moneda} sin prefijo {prefijo}")
            else:
                print(f"   ✅ Todas las cuentas {moneda} tienen prefijo {prefijo}")
        
        # 7. Verificar saldos
        print("\n6. Verificando saldos...")
        saldos_negativos = db(db.cuentas.saldo < 0).count()
        if saldos_negativos > 0:
            print(f"   ⚠️  Hay {saldos_negativos} cuentas con saldo negativo")
            verificacion['problemas'].append(f"Hay {saldos_negativos} cuentas con saldo negativo")
        else:
            print(f"   ✅ No hay cuentas con saldo negativo")
        
        # Resumen
        print("\n" + "-" * 80)
        if verificacion['problemas']:
            print(f"⚠️  Se encontraron {len(verificacion['problemas'])} problemas durante la verificación")
        else:
            print("✅ Todas las verificaciones pasaron correctamente")
        
        return verificacion
        
    except Exception as e:
        print(f"\n❌ ERROR durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
        return verificacion

# -------------------------------------------------------------------------
# FUNCIÓN DE GENERACIÓN DE REPORTE FINAL
# -------------------------------------------------------------------------

def generar_reporte_final(backup_path, stats, es_valida, problemas, verificacion):
    """
    Genera un reporte final completo de la migración
    """
    print("\n" + "=" * 80)
    print("GENERACIÓN DE REPORTE FINAL")
    print("=" * 80)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_reporte = f"reporte_migracion_produccion_{timestamp}.txt"
    
    reporte = []
    reporte.append("=" * 80)
    reporte.append("REPORTE DE MIGRACIÓN EN PRODUCCIÓN")
    reporte.append("Sistema de Divisas Bancario")
    reporte.append("=" * 80)
    reporte.append(f"\nFecha y Hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    reporte.append(f"Estado: {'✅ EXITOSA' if es_valida else '❌ CON PROBLEMAS'}")
    
    reporte.append("\n" + "-" * 80)
    reporte.append("1. BACKUP")
    reporte.append("-" * 80)
    reporte.append(f"\nBackup realizado: {'✅ Sí' if backup_path else '❌ No'}")
    if backup_path:
        reporte.append(f"Ubicación: {backup_path}")
    
    reporte.append("\n" + "-" * 80)
    reporte.append("2. ESTADÍSTICAS DE MIGRACIÓN")
    reporte.append("-" * 80)
    reporte.append(f"\nCuentas procesadas: {stats['cuentas_procesadas']}")
    reporte.append(f"Cuentas creadas: {stats['cuentas_creadas']}")
    reporte.append(f"\nDesglose por moneda:")
    reporte.append(f"  - VES: {stats['cuentas_con_ves']}")
    reporte.append(f"  - USD: {stats['cuentas_con_usd']}")
    reporte.append(f"  - EUR: {stats['cuentas_con_eur']}")
    reporte.append(f"  - USDT: {stats['cuentas_con_usdt']}")
    
    reporte.append("\n" + "-" * 80)
    reporte.append("3. SALDOS TOTALES")
    reporte.append("-" * 80)
    reporte.append("\nANTES:")
    for moneda, saldo in stats['saldo_total_antes'].items():
        reporte.append(f"  {moneda}: {saldo:,.4f}")
    reporte.append("\nDESPUÉS:")
    for moneda, saldo in stats['saldo_total_despues'].items():
        reporte.append(f"  {moneda}: {saldo:,.4f}")
    
    reporte.append("\n" + "-" * 80)
    reporte.append("4. VERIFICACIÓN DE CUENTAS")
    reporte.append("-" * 80)
    reporte.append(f"\nTotal de cuentas: {verificacion['total_cuentas']}")
    reporte.append(f"Clientes con cuentas: {verificacion['clientes_con_cuentas']}")
    reporte.append(f"Cuentas sin cliente: {verificacion['cuentas_sin_cliente']}")
    reporte.append(f"Números duplicados: {len(verificacion['numeros_duplicados'])}")
    
    if problemas or verificacion['problemas']:
        reporte.append("\n" + "-" * 80)
        reporte.append("5. PROBLEMAS ENCONTRADOS")
        reporte.append("-" * 80)
        todos_problemas = problemas + verificacion['problemas']
        for i, problema in enumerate(todos_problemas, 1):
            reporte.append(f"\n{i}. {problema}")
    
    reporte.append("\n" + "=" * 80)
    reporte.append("FIN DEL REPORTE")
    reporte.append("=" * 80)
    
    # Guardar reporte
    reporte_texto = "\n".join(reporte)
    
    try:
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            f.write(reporte_texto)
        print(f"\n✅ Reporte guardado en: {archivo_reporte}")
    except Exception as e:
        print(f"\n⚠️  No se pudo guardar el reporte: {str(e)}")
    
    print("\n" + reporte_texto)
    
    return archivo_reporte

# -------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL
# -------------------------------------------------------------------------

def main():
    """
    Función principal que ejecuta todos los pasos de la migración
    """
    print("\n" + "=" * 80)
    print("EJECUCIÓN DE MIGRACIÓN EN PRODUCCIÓN")
    print("Sistema de Divisas Bancario")
    print("=" * 80)
    print(f"\nFecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar contexto
    try:
        if 'db' not in globals():
            print("\n❌ Error: Este script debe ejecutarse con web2py")
            print("   Uso: python web2py.py -S sistema_divisas -M -R ejecutar_migracion_produccion.py")
            return
        
        if 'cuentas' not in db.tables:
            print("\n❌ Error: La tabla 'cuentas' no existe")
            return
        
        print("\n✅ Contexto verificado correctamente")
        
    except Exception as e:
        print(f"\n❌ Error al verificar contexto: {str(e)}")
        return
    
    # Confirmación del usuario
    print("\n" + "=" * 80)
    print("⚠️  ADVERTENCIA")
    print("=" * 80)
    print("\nEsta operación realizará cambios permanentes en la base de datos.")
    print("Se recomienda:")
    print("  1. Detener el servidor web si está en producción")
    print("  2. Asegurarse de que no hay usuarios conectados")
    print("  3. Tener un backup adicional manual")
    
    respuesta = input("\n¿Desea continuar? (escriba 'SI' para confirmar): ")
    
    if respuesta.strip().upper() != 'SI':
        print("\n❌ Migración cancelada por el usuario")
        return
    
    # Ejecutar pasos
    backup_path = None
    stats = None
    es_valida = False
    problemas = []
    verificacion = {}
    
    try:
        # Paso 1: Backup
        exitoso_backup, backup_path = realizar_backup_completo()
        if not exitoso_backup:
            print("\n❌ No se pudo realizar el backup. Abortando migración.")
            return
        
        # Paso 2: Migración
        stats = ejecutar_migracion()
        if stats is None:
            print("\n❌ Error en la migración. Abortando.")
            return
        
        # Paso 3: Validación
        es_valida, problemas = validar_integridad_datos(stats)
        
        # Paso 4: Verificación
        verificacion = verificar_cuentas_creadas()
        
        # Generar reporte final
        archivo_reporte = generar_reporte_final(backup_path, stats, es_valida, problemas, verificacion)
        
        # Mensaje final
        print("\n" + "=" * 80)
        if es_valida and not verificacion['problemas']:
            print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        else:
            print("⚠️  MIGRACIÓN COMPLETADA CON ADVERTENCIAS")
        print("=" * 80)
        
        print(f"\n📊 Resumen:")
        print(f"   - Backup: {backup_path}")
        print(f"   - Cuentas procesadas: {stats['cuentas_procesadas']}")
        print(f"   - Cuentas creadas: {stats['cuentas_creadas']}")
        print(f"   - Total cuentas en BD: {verificacion['total_cuentas']}")
        print(f"   - Reporte: {archivo_reporte}")
        
        if not es_valida or verificacion['problemas']:
            print(f"\n⚠️  Revise el reporte para más detalles sobre los problemas encontrados")
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n⚠️  Se recomienda restaurar el backup si es necesario")
        if backup_path:
            print(f"   Backup disponible en: {backup_path}")

# -------------------------------------------------------------------------
# Ejecutar
# -------------------------------------------------------------------------

if __name__ == '__main__':
    main()
