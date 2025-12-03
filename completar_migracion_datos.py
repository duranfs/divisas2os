# -*- coding: utf-8 -*-
"""
Script para completar la migración de datos
Migra los saldos de los campos antiguos al nuevo modelo
"""

import sqlite3
import os
from decimal import Decimal
from datetime import datetime

print("\n" + "=" * 80)
print("COMPLETAR MIGRACIÓN DE DATOS")
print("Sistema de Divisas Bancario")
print("=" * 80)
print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Ruta a la base de datos
db_path = r'C:\web2py\applications\divisas2os\databases\storage.sqlite'

if not os.path.exists(db_path):
    print(f"\n❌ No se encontró la base de datos en: {db_path}")
    exit(1)

# Hacer backup antes de continuar
print("\n" + "=" * 80)
print("PASO 1: BACKUP DE LA BASE DE DATOS")
print("=" * 80)

backup_dir = r'C:\web2py\applications\divisas2os\backups'
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_path = os.path.join(backup_dir, f'storage_completar_migracion_{timestamp}.sqlite')

import shutil
shutil.copy2(db_path, backup_path)
print(f"\n✅ Backup creado: {backup_path}")

# Conectar a la base de datos
print("\n" + "=" * 80)
print("PASO 2: ANÁLISIS DE DATOS ACTUALES")
print("=" * 80)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Obtener todas las cuentas
cursor.execute("""
    SELECT id, cliente_id, numero_cuenta, tipo_cuenta, moneda,
           saldo, saldo_ves, saldo_usd, saldo_eur, saldo_usdt
    FROM cuentas
    ORDER BY id
""")

cuentas = cursor.fetchall()

print(f"\nTotal de cuentas: {len(cuentas)}")

# Analizar qué cuentas necesitan migración
cuentas_a_migrar = []
cuentas_con_saldo_nuevo = 0

for cuenta in cuentas:
    id_cuenta, cliente_id, numero_cuenta, tipo_cuenta, moneda, saldo, saldo_ves, saldo_usd, saldo_eur, saldo_usdt = cuenta
    
    # Si el nuevo campo saldo ya tiene valor > 0, no migrar
    if saldo and float(saldo) > 0:
        cuentas_con_saldo_nuevo += 1
        continue
    
    # Si hay saldos en campos antiguos, necesita migración
    if (saldo_ves and float(saldo_ves) > 0) or \
       (saldo_usd and float(saldo_usd) > 0) or \
       (saldo_eur and float(saldo_eur) > 0) or \
       (saldo_usdt and float(saldo_usdt) > 0):
        cuentas_a_migrar.append(cuenta)

print(f"\nCuentas con saldo en nuevo campo: {cuentas_con_saldo_nuevo}")
print(f"Cuentas que necesitan migración: {len(cuentas_a_migrar)}")

if len(cuentas_a_migrar) == 0:
    print("\n✅ No hay cuentas que necesiten migración de datos")
    print("   Todos los saldos ya están en el nuevo campo")
    conn.close()
    exit(0)

# Mostrar detalles de cuentas a migrar
print("\nDetalles de cuentas a migrar:")
print("-" * 80)
for cuenta in cuentas_a_migrar:
    id_cuenta, cliente_id, numero_cuenta, tipo_cuenta, moneda, saldo, saldo_ves, saldo_usd, saldo_eur, saldo_usdt = cuenta
    print(f"\nCuenta ID {id_cuenta} - {numero_cuenta}")
    print(f"  Moneda actual: {moneda}")
    print(f"  Saldos antiguos:")
    if saldo_ves and float(saldo_ves) > 0:
        print(f"    VES: {float(saldo_ves):,.2f}")
    if saldo_usd and float(saldo_usd) > 0:
        print(f"    USD: {float(saldo_usd):,.2f}")
    if saldo_eur and float(saldo_eur) > 0:
        print(f"    EUR: {float(saldo_eur):,.2f}")
    if saldo_usdt and float(saldo_usdt) > 0:
        print(f"    USDT: {float(saldo_usdt):,.2f}")

# Confirmación
print("\n" + "=" * 80)
print("⚠️  ADVERTENCIA")
print("=" * 80)
print("\nEsta operación:")
print("  1. Migrará los saldos de los campos antiguos al nuevo campo 'saldo'")
print("  2. Creará cuentas adicionales para monedas con saldo > 0")
print("  3. Actualizará la base de datos de forma permanente")

respuesta = input("\n¿Desea continuar? (escriba 'SI' para confirmar): ")

if respuesta.strip().upper() != 'SI':
    print("\n❌ Migración cancelada por el usuario")
    conn.close()
    exit(0)

# Ejecutar migración
print("\n" + "=" * 80)
print("PASO 3: EJECUTAR MIGRACIÓN DE DATOS")
print("=" * 80)

import random

def generar_numero_cuenta_por_moneda(moneda, cursor):
    """Genera número de cuenta único con prefijo por moneda"""
    prefijos = {
        'VES': '01',
        'USD': '02',
        'EUR': '03',
        'USDT': '04'
    }
    
    prefijo = prefijos.get(moneda, '01')
    
    for intento in range(100):
        digitos = ''.join([str(random.randint(0, 9)) for _ in range(18)])
        numero_cuenta = prefijo + digitos
        
        # Verificar unicidad
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE numero_cuenta = ?", (numero_cuenta,))
        if cursor.fetchone()[0] == 0:
            return numero_cuenta
    
    raise Exception(f"No se pudo generar número de cuenta único para moneda {moneda}")

stats = {
    'cuentas_actualizadas': 0,
    'cuentas_creadas': 0,
    'errores': []
}

try:
    for cuenta in cuentas_a_migrar:
        id_cuenta, cliente_id, numero_cuenta, tipo_cuenta, moneda, saldo, saldo_ves, saldo_usd, saldo_eur, saldo_usdt = cuenta
        
        print(f"\nProcesando cuenta {numero_cuenta}...")
        
        # Obtener saldos
        saldos = {
            'VES': float(saldo_ves or 0),
            'USD': float(saldo_usd or 0),
            'EUR': float(saldo_eur or 0),
            'USDT': float(saldo_usdt or 0)
        }
        
        # Si la cuenta actual es VES, actualizar su saldo
        if moneda == 'VES' and saldos['VES'] > 0:
            cursor.execute("""
                UPDATE cuentas
                SET saldo = ?
                WHERE id = ?
            """, (saldos['VES'], id_cuenta))
            print(f"  ✅ Actualizada cuenta VES con saldo {saldos['VES']:,.2f}")
            stats['cuentas_actualizadas'] += 1
        
        # Crear cuentas para otras monedas con saldo > 0
        for moneda_saldo, valor_saldo in saldos.items():
            if valor_saldo > 0 and moneda_saldo != 'VES':
                # Verificar si ya existe cuenta para esta moneda
                cursor.execute("""
                    SELECT COUNT(*) FROM cuentas
                    WHERE cliente_id = ? AND moneda = ? AND estado = 'activa'
                """, (cliente_id, moneda_saldo))
                
                if cursor.fetchone()[0] == 0:
                    # Crear nueva cuenta
                    nuevo_numero = generar_numero_cuenta_por_moneda(moneda_saldo, cursor)
                    
                    cursor.execute("""
                        INSERT INTO cuentas
                        (cliente_id, numero_cuenta, tipo_cuenta, moneda, saldo,
                         saldo_ves, saldo_usd, saldo_eur, saldo_usdt,
                         estado, fecha_creacion)
                        VALUES (?, ?, ?, ?, ?, 0, 0, 0, 0, 'activa', datetime('now'))
                    """, (cliente_id, nuevo_numero, tipo_cuenta, moneda_saldo, valor_saldo))
                    
                    print(f"  ✅ Creada cuenta {moneda_saldo} con saldo {valor_saldo:,.2f}")
                    stats['cuentas_creadas'] += 1
    
    # Commit de cambios
    conn.commit()
    print("\n✅ Cambios guardados en la base de datos")
    
except Exception as e:
    print(f"\n❌ ERROR durante la migración: {str(e)}")
    conn.rollback()
    import traceback
    traceback.print_exc()
    conn.close()
    exit(1)

# Verificación final
print("\n" + "=" * 80)
print("PASO 4: VERIFICACIÓN FINAL")
print("=" * 80)

cursor.execute("""
    SELECT moneda, COUNT(*) as cantidad, SUM(saldo) as total
    FROM cuentas
    WHERE moneda IS NOT NULL AND moneda != ''
    GROUP BY moneda
    ORDER BY moneda
""")

resultados = cursor.fetchall()

print("\nCuentas por moneda (después de migración):")
for moneda, cantidad, total in resultados:
    print(f"  {moneda}: {cantidad} cuentas, Total: {total:,.4f}")

# Verificar saldos antiguos
cursor.execute("SELECT SUM(saldo_ves), SUM(saldo_usd), SUM(saldo_eur), SUM(saldo_usdt) FROM cuentas")
totales_antiguos = cursor.fetchone()

print("\nSaldos en campos antiguos (deberían estar en 0 o ser iguales):")
print(f"  saldo_ves: {totales_antiguos[0] or 0:,.2f}")
print(f"  saldo_usd: {totales_antiguos[1] or 0:,.2f}")
print(f"  saldo_eur: {totales_antiguos[2] or 0:,.2f}")
print(f"  saldo_usdt: {totales_antiguos[3] or 0:,.2f}")

conn.close()

# Resumen final
print("\n" + "=" * 80)
print("RESUMEN DE MIGRACIÓN")
print("=" * 80)

print(f"\n✅ Migración completada exitosamente")
print(f"\nEstadísticas:")
print(f"  - Cuentas actualizadas: {stats['cuentas_actualizadas']}")
print(f"  - Cuentas creadas: {stats['cuentas_creadas']}")
print(f"  - Backup: {backup_path}")

if stats['errores']:
    print(f"\n⚠️  Errores encontrados: {len(stats['errores'])}")
    for error in stats['errores']:
        print(f"  - {error}")

print("\n" + "=" * 80)
print("✅ MIGRACIÓN DE DATOS COMPLETADA")
print("=" * 80)
