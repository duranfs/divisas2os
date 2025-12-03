# -*- coding: utf-8 -*-
"""
Script de Validación Post-Migración
Sistema de Divisas Bancario

Este script valida que la migración se haya completado correctamente
y que el sistema esté funcionando con el nuevo modelo de cuentas.

Uso:
    python web2py.py -S sistema_divisas -M -R validar_migracion_completa.py

Autor: Sistema de Divisas Bancario
Fecha: 2025-11-25
"""

from decimal import Decimal
import datetime

def validar_estructura_cuentas():
    """Valida que todas las cuentas tengan la estructura correcta"""
    print("\n" + "=" * 80)
    print("1. VALIDACIÓN DE ESTRUCTURA DE CUENTAS")
    print("=" * 80)
    
    problemas = []
    
    # Verificar que todas las cuentas tienen moneda asignada
    cuentas_sin_moneda = db(
        (db.cuentas.moneda == None) | (db.cuentas.moneda == '')
    ).count()
    
    if cuentas_sin_moneda > 0:
        problema = f"❌ Hay {cuentas_sin_moneda} cuentas sin moneda asignada"
        print(f"\n{problema}")
        problemas.append(problema)
    else:
        print("\n✅ Todas las cuentas tienen moneda asignada")
    
    # Verificar que todas las cuentas tienen saldo definido
    cuentas_sin_saldo = db(db.cuentas.saldo == None).count()
    
    if cuentas_sin_saldo > 0:
        problema = f"❌ Hay {cuentas_sin_saldo} cuentas sin saldo definido"
        print(f"{problema}")
        problemas.append(problema)
    else:
        print("✅ Todas las cuentas tienen saldo definido")
    
    # Verificar monedas válidas
    monedas_validas = ['VES', 'USD', 'EUR', 'USDT']
    cuentas_moneda_invalida = db(
        ~db.cuentas.moneda.belongs(monedas_validas)
    ).count()
    
    if cuentas_moneda_invalida > 0:
        problema = f"❌ Hay {cuentas_moneda_invalida} cuentas con moneda inválida"
        print(f"{problema}")
        problemas.append(problema)
    else:
        print("✅ Todas las cuentas tienen monedas válidas")
    
    return problemas

def validar_unicidad_cuentas():
    """Valida que no haya cuentas duplicadas por cliente y moneda"""
    print("\n" + "=" * 80)
    print("2. VALIDACIÓN DE UNICIDAD DE CUENTAS")
    print("=" * 80)
    
    problemas = []
    
    # Buscar clientes con múltiples cuentas activas de la misma moneda
    clientes = db(db.clientes.id > 0).select()
    
    duplicados_encontrados = 0
    
    for cliente in clientes:
        for moneda in ['VES', 'USD', 'EUR', 'USDT']:
            cuentas_moneda = db(
                (db.cuentas.cliente_id == cliente.id) &
                (db.cuentas.moneda == moneda) &
                (db.cuentas.estado == 'activa')
            ).count()
            
            if cuentas_moneda > 1:
                problema = f"❌ Cliente {cliente.id} tiene {cuentas_moneda} cuentas {moneda} activas"
                print(f"\n{problema}")
                problemas.append(problema)
                duplicados_encontrados += 1
    
    if duplicados_encontrados == 0:
        print("\n✅ No hay cuentas duplicadas por cliente y moneda")
    else:
        print(f"\n⚠️  Se encontraron {duplicados_encontrados} casos de duplicación")
    
    return problemas

def validar_numeros_cuenta():
    """Valida que los números de cuenta tengan el formato correcto"""
    print("\n" + "=" * 80)
    print("3. VALIDACIÓN DE NÚMEROS DE CUENTA")
    print("=" * 80)
    
    problemas = []
    
    prefijos = {
        'VES': '01',
        'USD': '02',
        'EUR': '03',
        'USDT': '04'
    }
    
    for moneda, prefijo in prefijos.items():
        cuentas = db(db.cuentas.moneda == moneda).select()
        
        sin_prefijo = 0
        longitud_incorrecta = 0
        
        for cuenta in cuentas:
            # Verificar prefijo
            if not cuenta.numero_cuenta.startswith(prefijo):
                sin_prefijo += 1
            
            # Verificar longitud (debe ser 20 dígitos)
            if len(cuenta.numero_cuenta) != 20:
                longitud_incorrecta += 1
        
        if sin_prefijo > 0:
            problema = f"❌ {sin_prefijo} cuentas {moneda} sin prefijo {prefijo}"
            print(f"\n{problema}")
            problemas.append(problema)
        else:
            print(f"\n✅ Todas las cuentas {moneda} tienen prefijo {prefijo}")
        
        if longitud_incorrecta > 0:
            problema = f"❌ {longitud_incorrecta} cuentas {moneda} con longitud incorrecta"
            print(f"{problema}")
            problemas.append(problema)
        else:
            print(f"✅ Todas las cuentas {moneda} tienen 20 dígitos")
    
    # Verificar unicidad de números
    numeros = db(db.cuentas.id > 0).select(db.cuentas.numero_cuenta)
    numeros_lista = [n.numero_cuenta for n in numeros]
    numeros_unicos = set(numeros_lista)
    
    if len(numeros_lista) != len(numeros_unicos):
        duplicados = [n for n in numeros_unicos if numeros_lista.count(n) > 1]
        problema = f"❌ Hay {len(duplicados)} números de cuenta duplicados"
        print(f"\n{problema}")
        problemas.append(problema)
    else:
        print(f"\n✅ Todos los números de cuenta son únicos")
    
    return problemas

def validar_saldos():
    """Valida que los saldos sean consistentes"""
    print("\n" + "=" * 80)
    print("4. VALIDACIÓN DE SALDOS")
    print("=" * 80)
    
    problemas = []
    
    # Verificar saldos negativos
    saldos_negativos = db(db.cuentas.saldo < 0).count()
    
    if saldos_negativos > 0:
        problema = f"⚠️  Hay {saldos_negativos} cuentas con saldo negativo"
        print(f"\n{problema}")
        problemas.append(problema)
    else:
        print("\n✅ No hay cuentas con saldo negativo")
    
    # Calcular totales por moneda
    print("\n💰 Saldos totales por moneda:")
    
    for moneda in ['VES', 'USD', 'EUR', 'USDT']:
        cuentas = db(db.cuentas.moneda == moneda).select()
        total = sum([Decimal(str(c.saldo or 0)) for c in cuentas])
        cantidad = len(cuentas)
        
        print(f"   {moneda}: {total:,.4f} ({cantidad} cuentas)")
    
    # Verificar que los campos antiguos estén en 0
    print("\n🔍 Verificando campos antiguos (deprecated):")
    
    campos_antiguos = ['saldo_ves', 'saldo_usd', 'saldo_eur', 'saldo_usdt']
    campos_con_datos = 0
    
    for campo in campos_antiguos:
        cuentas_con_saldo = db(db.cuentas[campo] > 0).count()
        if cuentas_con_saldo > 0:
            print(f"   ⚠️  {cuentas_con_saldo} cuentas tienen {campo} > 0")
            campos_con_datos += 1
        else:
            print(f"   ✅ Todas las cuentas tienen {campo} = 0")
    
    if campos_con_datos > 0:
        problema = f"⚠️  Hay campos antiguos con datos (esto es normal si aún no se han limpiado)"
        problemas.append(problema)
    
    return problemas

def validar_clientes():
    """Valida que todos los clientes tengan al menos una cuenta VES"""
    print("\n" + "=" * 80)
    print("5. VALIDACIÓN DE CLIENTES")
    print("=" * 80)
    
    problemas = []
    
    clientes = db(db.clientes.id > 0).select()
    total_clientes = len(clientes)
    
    print(f"\n📊 Total de clientes: {total_clientes}")
    
    clientes_sin_cuenta_ves = 0
    clientes_sin_cuentas = 0
    
    for cliente in clientes:
        # Verificar que tenga al menos una cuenta
        cuentas = db(db.cuentas.cliente_id == cliente.id).count()
        
        if cuentas == 0:
            clientes_sin_cuentas += 1
            continue
        
        # Verificar que tenga cuenta VES
        cuenta_ves = db(
            (db.cuentas.cliente_id == cliente.id) &
            (db.cuentas.moneda == 'VES') &
            (db.cuentas.estado == 'activa')
        ).count()
        
        if cuenta_ves == 0:
            clientes_sin_cuenta_ves += 1
    
    if clientes_sin_cuentas > 0:
        problema = f"⚠️  {clientes_sin_cuentas} clientes no tienen ninguna cuenta"
        print(f"\n{problema}")
        problemas.append(problema)
    else:
        print("\n✅ Todos los clientes tienen al menos una cuenta")
    
    if clientes_sin_cuenta_ves > 0:
        problema = f"⚠️  {clientes_sin_cuenta_ves} clientes no tienen cuenta VES"
        print(f"{problema}")
        problemas.append(problema)
    else:
        print("✅ Todos los clientes tienen cuenta VES")
    
    # Estadísticas de cuentas por cliente
    print("\n📈 Estadísticas de cuentas por cliente:")
    
    for moneda in ['VES', 'USD', 'EUR', 'USDT']:
        clientes_con_moneda = db(
            (db.cuentas.moneda == moneda) &
            (db.cuentas.estado == 'activa')
        ).select(db.cuentas.cliente_id, distinct=True)
        
        print(f"   Clientes con cuenta {moneda}: {len(clientes_con_moneda)}")
    
    return problemas

def validar_transacciones():
    """Valida que las transacciones tengan referencias correctas"""
    print("\n" + "=" * 80)
    print("6. VALIDACIÓN DE TRANSACCIONES")
    print("=" * 80)
    
    problemas = []
    
    total_transacciones = db(db.transacciones.id > 0).count()
    print(f"\n📊 Total de transacciones: {total_transacciones}")
    
    # Verificar transacciones con nuevos campos
    transacciones_con_cuentas = db(
        (db.transacciones.cuenta_origen_id != None) &
        (db.transacciones.cuenta_destino_id != None)
    ).count()
    
    print(f"\n✅ Transacciones con cuenta_origen_id y cuenta_destino_id: {transacciones_con_cuentas}")
    
    # Verificar transacciones antiguas
    transacciones_antiguas = db(
        (db.transacciones.cuenta_origen_id == None) |
        (db.transacciones.cuenta_destino_id == None)
    ).count()
    
    if transacciones_antiguas > 0:
        print(f"⚠️  Transacciones con modelo antiguo: {transacciones_antiguas}")
        print("   (Esto es normal si hay transacciones históricas)")
    
    # Verificar referencias válidas
    transacciones = db(
        (db.transacciones.cuenta_origen_id != None) &
        (db.transacciones.cuenta_destino_id != None)
    ).select()
    
    referencias_invalidas = 0
    
    for trans in transacciones:
        cuenta_origen = db.cuentas[trans.cuenta_origen_id]
        cuenta_destino = db.cuentas[trans.cuenta_destino_id]
        
        if not cuenta_origen or not cuenta_destino:
            referencias_invalidas += 1
    
    if referencias_invalidas > 0:
        problema = f"❌ {referencias_invalidas} transacciones con referencias inválidas"
        print(f"\n{problema}")
        problemas.append(problema)
    else:
        print(f"✅ Todas las transacciones tienen referencias válidas")
    
    return problemas

def generar_resumen_validacion(todos_problemas):
    """Genera un resumen de la validación"""
    print("\n" + "=" * 80)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 80)
    
    if not todos_problemas:
        print("\n✅ ¡VALIDACIÓN EXITOSA!")
        print("   Todas las verificaciones pasaron correctamente.")
        print("   El sistema está listo para operar con el nuevo modelo de cuentas.")
    else:
        print(f"\n⚠️  Se encontraron {len(todos_problemas)} problemas:")
        for i, problema in enumerate(todos_problemas, 1):
            print(f"\n{i}. {problema}")
        
        print("\n📋 Recomendaciones:")
        print("   - Revise los problemas encontrados")
        print("   - Corrija los problemas críticos antes de poner en producción")
        print("   - Los problemas menores pueden ser aceptables según el contexto")
    
    # Guardar reporte
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = f"validacion_migracion_{timestamp}.txt"
    
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE VALIDACIÓN POST-MIGRACIÓN\n")
            f.write("=" * 80 + "\n")
            f.write(f"\nFecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\nProblemas encontrados: {len(todos_problemas)}\n")
            
            if todos_problemas:
                f.write("\nDETALLE DE PROBLEMAS:\n")
                f.write("-" * 80 + "\n")
                for i, problema in enumerate(todos_problemas, 1):
                    f.write(f"\n{i}. {problema}\n")
            else:
                f.write("\n✅ Todas las validaciones pasaron correctamente\n")
        
        print(f"\n📄 Reporte guardado en: {archivo}")
    except Exception as e:
        print(f"\n⚠️  No se pudo guardar el reporte: {str(e)}")

def main():
    """Función principal de validación"""
    print("\n" + "=" * 80)
    print("VALIDACIÓN POST-MIGRACIÓN")
    print("Sistema de Divisas Bancario")
    print("=" * 80)
    print(f"\nFecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar contexto
    try:
        if 'db' not in globals():
            print("\n❌ Error: Este script debe ejecutarse con web2py")
            print("   Uso: python web2py.py -S sistema_divisas -M -R validar_migracion_completa.py")
            return
        
        if 'cuentas' not in db.tables:
            print("\n❌ Error: La tabla 'cuentas' no existe")
            return
        
        print("\n✅ Contexto verificado correctamente")
        
    except Exception as e:
        print(f"\n❌ Error al verificar contexto: {str(e)}")
        return
    
    # Ejecutar validaciones
    todos_problemas = []
    
    try:
        problemas = validar_estructura_cuentas()
        todos_problemas.extend(problemas)
        
        problemas = validar_unicidad_cuentas()
        todos_problemas.extend(problemas)
        
        problemas = validar_numeros_cuenta()
        todos_problemas.extend(problemas)
        
        problemas = validar_saldos()
        todos_problemas.extend(problemas)
        
        problemas = validar_clientes()
        todos_problemas.extend(problemas)
        
        problemas = validar_transacciones()
        todos_problemas.extend(problemas)
        
        # Generar resumen
        generar_resumen_validacion(todos_problemas)
        
    except Exception as e:
        print(f"\n❌ ERROR durante la validación: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
