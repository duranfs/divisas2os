# -*- coding: utf-8 -*-
"""
Script de Migración de Cuentas Multi-Moneda a Cuentas Individuales por Moneda

Este script migra el sistema de cuentas del modelo antiguo (una cuenta con múltiples saldos)
al nuevo modelo (una cuenta por moneda).

Uso:
    python web2py.py -S sistema_divisas -M -R migrar_cuentas.py

Autor: Sistema de Divisas Bancario
Fecha: 2025-11-25
"""

import datetime
import random
from decimal import Decimal

# -------------------------------------------------------------------------
# Función de Generación de Números de Cuenta
# -------------------------------------------------------------------------

def generar_numero_cuenta_por_moneda(moneda, db):
    """
    Genera número de cuenta único con prefijo por moneda
    
    Args:
        moneda: Código de moneda (VES, USD, EUR, USDT)
        db: Instancia de base de datos
        
    Returns:
        String con número de cuenta de 20 dígitos
    """
    prefijos = {
        'VES': '01',
        'USD': '02',
        'EUR': '03',
        'USDT': '04'
    }
    
    prefijo = prefijos.get(moneda, '01')
    
    # Generar 18 dígitos aleatorios
    max_intentos = 100
    for intento in range(max_intentos):
        digitos = ''.join([str(random.randint(0, 9)) for _ in range(18)])
        numero_cuenta = prefijo + digitos
        
        # Verificar unicidad
        if db(db.cuentas.numero_cuenta == numero_cuenta).count() == 0:
            return numero_cuenta
    
    # Si no se pudo generar después de max_intentos
    raise Exception(f"No se pudo generar número de cuenta único para moneda {moneda}")

# -------------------------------------------------------------------------
# Función Principal de Migración
# -------------------------------------------------------------------------

def migrar_cuentas_a_moneda_unica(db, dry_run=False):
    """
    Migra cuentas multi-moneda a cuentas individuales por moneda
    
    Args:
        db: Instancia de base de datos
        dry_run: Si es True, solo simula la migración sin hacer cambios
        
    Returns:
        Dict con estadísticas de la migración
    """
    print("=" * 80)
    print("MIGRACIÓN DE CUENTAS MULTI-MONEDA A CUENTAS INDIVIDUALES")
    print("=" * 80)
    
    if dry_run:
        print("\n⚠️  MODO SIMULACIÓN - No se realizarán cambios en la base de datos")
    else:
        print("\n✅ MODO REAL - Se realizarán cambios en la base de datos")
    
    print("\n" + "-" * 80)
    print("FASE 1: Preparación de Base de Datos")
    print("-" * 80)
    
    # 1. Verificar y agregar columnas nuevas si no existen
    try:
        # Verificar si las columnas ya existen
        test_query = db(db.cuentas.id > 0).select(
            db.cuentas.id, 
            db.cuentas.moneda, 
            db.cuentas.saldo,
            limitby=(0, 1)
        )
        print("✅ Columnas 'moneda' y 'saldo' ya existen")
    except Exception as e:
        print("⚠️  Columnas 'moneda' y 'saldo' no existen, agregándolas...")
        if not dry_run:
            try:
                db.executesql("ALTER TABLE cuentas ADD COLUMN moneda VARCHAR(10) DEFAULT 'VES'")
                db.executesql("ALTER TABLE cuentas ADD COLUMN saldo DECIMAL(15,4) DEFAULT 0")
                db.commit()
                print("✅ Columnas agregadas exitosamente")
            except Exception as alter_error:
                print(f"❌ Error al agregar columnas: {str(alter_error)}")
                return None
        else:
            print("   [SIMULACIÓN] Se agregarían las columnas 'moneda' y 'saldo'")
    
    print("\n" + "-" * 80)
    print("FASE 2: Análisis de Cuentas Existentes")
    print("-" * 80)
    
    # 2. Obtener todas las cuentas actuales
    cuentas_antiguas = db(db.cuentas.id > 0).select()
    total_cuentas_antiguas = len(cuentas_antiguas)
    
    print(f"\n📊 Total de cuentas a procesar: {total_cuentas_antiguas}")
    
    # Estadísticas
    stats = {
        'cuentas_procesadas': 0,
        'cuentas_creadas': 0,
        'cuentas_actualizadas': 0,
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
    
    # Calcular saldos totales antes de la migración
    for cuenta in cuentas_antiguas:
        stats['saldo_total_antes']['VES'] += Decimal(str(cuenta.saldo_ves or 0))
        stats['saldo_total_antes']['USD'] += Decimal(str(cuenta.saldo_usd or 0))
        stats['saldo_total_antes']['EUR'] += Decimal(str(cuenta.saldo_eur or 0))
        stats['saldo_total_antes']['USDT'] += Decimal(str(cuenta.saldo_usdt or 0))
    
    print("\n💰 Saldos totales ANTES de la migración:")
    for moneda, saldo in stats['saldo_total_antes'].items():
        print(f"   {moneda}: {saldo:,.4f}")
    
    print("\n" + "-" * 80)
    print("FASE 3: Migración de Cuentas")
    print("-" * 80)
    
    # 3. Procesar cada cuenta
    for idx, cuenta_antigua in enumerate(cuentas_antiguas, 1):
        try:
            cliente_id = cuenta_antigua.cliente_id
            print(f"\n[{idx}/{total_cuentas_antiguas}] Procesando cuenta {cuenta_antigua.numero_cuenta} (Cliente ID: {cliente_id})")
            
            # Obtener saldos de cada moneda
            monedas_saldos = {
                'VES': Decimal(str(cuenta_antigua.saldo_ves or 0)),
                'USD': Decimal(str(cuenta_antigua.saldo_usd or 0)),
                'EUR': Decimal(str(cuenta_antigua.saldo_eur or 0)),
                'USDT': Decimal(str(cuenta_antigua.saldo_usdt or 0))
            }
            
            # Mostrar saldos de la cuenta
            print(f"   Saldos: VES={monedas_saldos['VES']}, USD={monedas_saldos['USD']}, EUR={monedas_saldos['EUR']}, USDT={monedas_saldos['USDT']}")
            
            # Procesar cada moneda
            for moneda, saldo in monedas_saldos.items():
                # Siempre crear cuenta VES, para otras monedas solo si tienen saldo > 0
                if saldo > 0 or moneda == 'VES':
                    # Verificar si ya existe cuenta para esta moneda
                    cuenta_existente = db(
                        (db.cuentas.cliente_id == cliente_id) &
                        (db.cuentas.moneda == moneda) &
                        (db.cuentas.estado == 'activa')
                    ).select().first()
                    
                    if cuenta_existente:
                        print(f"   ⚠️  Ya existe cuenta {moneda} para este cliente")
                        continue
                    
                    # Determinar número de cuenta
                    if moneda == 'VES':
                        # Mantener número de cuenta original para VES
                        numero_cuenta = cuenta_antigua.numero_cuenta
                        print(f"   ✅ Creando cuenta {moneda} (manteniendo número original: {numero_cuenta})")
                    else:
                        # Generar nuevo número para otras monedas
                        if not dry_run:
                            numero_cuenta = generar_numero_cuenta_por_moneda(moneda, db)
                        else:
                            numero_cuenta = f"[SIMULADO-{moneda}]"
                        print(f"   ✅ Creando cuenta {moneda} (nuevo número: {numero_cuenta})")
                    
                    # Crear nueva cuenta
                    if not dry_run:
                        try:
                            nuevo_id = db.cuentas.insert(
                                cliente_id=cliente_id,
                                numero_cuenta=numero_cuenta,
                                tipo_cuenta=cuenta_antigua.tipo_cuenta,
                                moneda=moneda,
                                saldo=float(saldo),
                                estado='activa',
                                fecha_creacion=cuenta_antigua.fecha_creacion,
                                # Mantener campos antiguos en 0 para compatibilidad
                                saldo_ves=0,
                                saldo_usd=0,
                                saldo_eur=0,
                                saldo_usdt=0
                            )
                            stats['cuentas_creadas'] += 1
                            stats[f'cuentas_con_{moneda.lower()}'] += 1
                            stats['saldo_total_despues'][moneda] += saldo
                            print(f"      ✓ Cuenta creada con ID: {nuevo_id}")
                        except Exception as insert_error:
                            error_msg = f"Error al crear cuenta {moneda} para cliente {cliente_id}: {str(insert_error)}"
                            print(f"      ❌ {error_msg}")
                            stats['errores'].append(error_msg)
                    else:
                        print(f"      [SIMULACIÓN] Se crearía cuenta {moneda} con saldo {saldo}")
                        stats['cuentas_creadas'] += 1
                        stats[f'cuentas_con_{moneda.lower()}'] += 1
                        stats['saldo_total_despues'][moneda] += saldo
            
            stats['cuentas_procesadas'] += 1
            
        except Exception as e:
            error_msg = f"Error al procesar cuenta {cuenta_antigua.numero_cuenta}: {str(e)}"
            print(f"   ❌ {error_msg}")
            stats['errores'].append(error_msg)
    
    # Commit de cambios
    if not dry_run:
        try:
            db.commit()
            print("\n✅ Cambios guardados en la base de datos")
        except Exception as commit_error:
            print(f"\n❌ Error al guardar cambios: {str(commit_error)}")
            db.rollback()
            return None
    
    return stats

# -------------------------------------------------------------------------
# Función de Validación de Migración
# -------------------------------------------------------------------------

def validar_migracion(stats):
    """
    Valida que la migración se haya realizado correctamente
    
    Args:
        stats: Diccionario con estadísticas de la migración
        
    Returns:
        Tuple (bool, list) - (es_valida, lista_de_problemas)
    """
    print("\n" + "=" * 80)
    print("FASE 4: Validación de Migración")
    print("=" * 80)
    
    problemas = []
    
    # 1. Verificar que no se perdieron datos
    print("\n1. Verificando integridad de saldos...")
    
    for moneda in ['VES', 'USD', 'EUR', 'USDT']:
        saldo_antes = stats['saldo_total_antes'][moneda]
        saldo_despues = stats['saldo_total_despues'][moneda]
        
        diferencia = abs(saldo_antes - saldo_despues)
        
        if diferencia > Decimal('0.01'):  # Tolerancia de 0.01
            problema = f"❌ Diferencia en saldos de {moneda}: Antes={saldo_antes}, Después={saldo_despues}, Diferencia={diferencia}"
            print(f"   {problema}")
            problemas.append(problema)
        else:
            print(f"   ✅ {moneda}: Saldos coinciden (Antes={saldo_antes}, Después={saldo_despues})")
    
    # 2. Verificar que se crearon las cuentas esperadas
    print("\n2. Verificando creación de cuentas...")
    print(f"   ✅ Cuentas procesadas: {stats['cuentas_procesadas']}")
    print(f"   ✅ Cuentas creadas: {stats['cuentas_creadas']}")
    print(f"   ✅ Cuentas VES: {stats['cuentas_con_ves']}")
    print(f"   ✅ Cuentas USD: {stats['cuentas_con_usd']}")
    print(f"   ✅ Cuentas EUR: {stats['cuentas_con_eur']}")
    print(f"   ✅ Cuentas USDT: {stats['cuentas_con_usdt']}")
    
    # 3. Verificar errores
    if stats['errores']:
        print(f"\n3. ⚠️  Se encontraron {len(stats['errores'])} errores durante la migración:")
        for error in stats['errores']:
            print(f"   - {error}")
            problemas.append(error)
    else:
        print("\n3. ✅ No se encontraron errores durante la migración")
    
    # Resultado final
    es_valida = len(problemas) == 0
    
    return es_valida, problemas

# -------------------------------------------------------------------------
# Función de Generación de Reporte
# -------------------------------------------------------------------------

def generar_reporte_migracion(stats, es_valida, problemas, archivo='reporte_migracion.txt'):
    """
    Genera un reporte detallado de la migración
    
    Args:
        stats: Estadísticas de la migración
        es_valida: Si la migración fue válida
        problemas: Lista de problemas encontrados
        archivo: Nombre del archivo de reporte
    """
    print("\n" + "=" * 80)
    print("FASE 5: Generación de Reporte")
    print("=" * 80)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    reporte = []
    reporte.append("=" * 80)
    reporte.append("REPORTE DE MIGRACIÓN DE CUENTAS")
    reporte.append("=" * 80)
    reporte.append(f"\nFecha y Hora: {timestamp}")
    reporte.append(f"\nEstado: {'✅ EXITOSA' if es_valida else '❌ CON PROBLEMAS'}")
    
    reporte.append("\n" + "-" * 80)
    reporte.append("ESTADÍSTICAS")
    reporte.append("-" * 80)
    reporte.append(f"\nCuentas procesadas: {stats['cuentas_procesadas']}")
    reporte.append(f"Cuentas creadas: {stats['cuentas_creadas']}")
    reporte.append(f"Cuentas actualizadas: {stats['cuentas_actualizadas']}")
    reporte.append(f"\nDesglose por moneda:")
    reporte.append(f"  - Cuentas VES: {stats['cuentas_con_ves']}")
    reporte.append(f"  - Cuentas USD: {stats['cuentas_con_usd']}")
    reporte.append(f"  - Cuentas EUR: {stats['cuentas_con_eur']}")
    reporte.append(f"  - Cuentas USDT: {stats['cuentas_con_usdt']}")
    
    reporte.append("\n" + "-" * 80)
    reporte.append("SALDOS TOTALES")
    reporte.append("-" * 80)
    reporte.append("\nANTES de la migración:")
    for moneda, saldo in stats['saldo_total_antes'].items():
        reporte.append(f"  {moneda}: {saldo:,.4f}")
    
    reporte.append("\nDESPUÉS de la migración:")
    for moneda, saldo in stats['saldo_total_despues'].items():
        reporte.append(f"  {moneda}: {saldo:,.4f}")
    
    reporte.append("\nDIFERENCIAS:")
    for moneda in ['VES', 'USD', 'EUR', 'USDT']:
        diferencia = stats['saldo_total_despues'][moneda] - stats['saldo_total_antes'][moneda]
        reporte.append(f"  {moneda}: {diferencia:,.4f}")
    
    if problemas:
        reporte.append("\n" + "-" * 80)
        reporte.append("PROBLEMAS ENCONTRADOS")
        reporte.append("-" * 80)
        for i, problema in enumerate(problemas, 1):
            reporte.append(f"\n{i}. {problema}")
    
    reporte.append("\n" + "=" * 80)
    reporte.append("FIN DEL REPORTE")
    reporte.append("=" * 80)
    
    # Guardar reporte en archivo
    reporte_texto = "\n".join(reporte)
    
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(reporte_texto)
        print(f"\n✅ Reporte guardado en: {archivo}")
    except Exception as e:
        print(f"\n⚠️  No se pudo guardar el reporte en archivo: {str(e)}")
    
    # Mostrar reporte en consola
    print("\n" + reporte_texto)
    
    return reporte_texto

# -------------------------------------------------------------------------
# Función Principal de Ejecución
# -------------------------------------------------------------------------

def main():
    """
    Función principal que ejecuta la migración con confirmación del usuario
    """
    print("\n" + "=" * 80)
    print("SCRIPT DE MIGRACIÓN DE CUENTAS")
    print("Sistema de Divisas Bancario")
    print("=" * 80)
    
    # Verificar que estamos en el contexto correcto
    try:
        # Verificar que db existe
        if 'db' not in globals():
            print("\n❌ Error: Este script debe ejecutarse con web2py")
            print("   Uso: python web2py.py -S sistema_divisas -M -R migrar_cuentas.py")
            return
        
        # Verificar que la tabla cuentas existe
        if 'cuentas' not in db.tables:
            print("\n❌ Error: La tabla 'cuentas' no existe en la base de datos")
            return
        
        print("\n✅ Contexto de web2py detectado correctamente")
        print(f"✅ Base de datos: {db._uri}")
        
    except Exception as e:
        print(f"\n❌ Error al verificar contexto: {str(e)}")
        return
    
    # Primero ejecutar en modo simulación
    print("\n" + "-" * 80)
    print("PASO 1: Simulación de Migración")
    print("-" * 80)
    print("\nEjecutando migración en modo simulación...")
    
    stats_simulacion = migrar_cuentas_a_moneda_unica(db, dry_run=True)
    
    if stats_simulacion is None:
        print("\n❌ Error en la simulación. Abortando migración.")
        return
    
    # Validar simulación
    es_valida_sim, problemas_sim = validar_migracion(stats_simulacion)
    
    if not es_valida_sim:
        print("\n⚠️  La simulación detectó problemas potenciales.")
        print("   Se recomienda revisar antes de continuar.")
    
    # Solicitar confirmación
    print("\n" + "=" * 80)
    print("CONFIRMACIÓN REQUERIDA")
    print("=" * 80)
    print("\n⚠️  ADVERTENCIA: Esta operación modificará la estructura de la base de datos")
    print("   y creará nuevas cuentas basadas en los saldos existentes.")
    print("\n   Asegúrese de haber realizado un backup de la base de datos antes de continuar.")
    
    respuesta = input("\n¿Desea continuar con la migración REAL? (escriba 'SI' para confirmar): ")
    
    if respuesta.strip().upper() != 'SI':
        print("\n❌ Migración cancelada por el usuario")
        return
    
    # Ejecutar migración real
    print("\n" + "-" * 80)
    print("PASO 2: Migración Real")
    print("-" * 80)
    print("\nEjecutando migración REAL...")
    
    stats_real = migrar_cuentas_a_moneda_unica(db, dry_run=False)
    
    if stats_real is None:
        print("\n❌ Error en la migración real. Los cambios han sido revertidos.")
        return
    
    # Validar migración real
    es_valida_real, problemas_real = validar_migracion(stats_real)
    
    # Generar reporte
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_reporte = f"reporte_migracion_{timestamp}.txt"
    generar_reporte_migracion(stats_real, es_valida_real, problemas_real, archivo_reporte)
    
    # Mensaje final
    print("\n" + "=" * 80)
    if es_valida_real:
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
    else:
        print("⚠️  MIGRACIÓN COMPLETADA CON ADVERTENCIAS")
    print("=" * 80)
    
    print(f"\n📊 Resumen:")
    print(f"   - Cuentas procesadas: {stats_real['cuentas_procesadas']}")
    print(f"   - Cuentas creadas: {stats_real['cuentas_creadas']}")
    print(f"   - Errores: {len(stats_real['errores'])}")
    
    if not es_valida_real:
        print(f"\n⚠️  Se encontraron {len(problemas_real)} problemas. Revise el reporte para más detalles.")
    
    print(f"\n📄 Reporte completo guardado en: {archivo_reporte}")

# -------------------------------------------------------------------------
# Ejecutar script
# -------------------------------------------------------------------------

if __name__ == '__main__':
    main()
