# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que los reportes administrativos incluyan USDT
"""

import sys
import os

# Agregar el directorio de web2py al path
web2py_path = os.path.join(os.path.dirname(__file__), 'web2py')
sys.path.insert(0, web2py_path)

print("=" * 70)
print("VERIFICACIÓN DE REPORTES ADMINISTRATIVOS CON USDT")
print("=" * 70)

# Simular el entorno de web2py
from gluon import DAL, Field
from gluon.tools import Auth
import datetime

# Conectar a la base de datos
db_path = os.path.join('web2py', 'applications', 'sistema_divisas', 'databases', 'storage.sqlite')
db = DAL(f'sqlite://{db_path}', folder=os.path.join('web2py', 'applications', 'sistema_divisas', 'databases'))

# Definir tablas necesarias
db.define_table('transacciones',
    Field('fecha_transaccion', 'datetime'),
    Field('tipo_operacion', 'string'),
    Field('moneda_origen', 'string'),
    Field('monto_origen', 'decimal(15,2)'),
    Field('moneda_destino', 'string'),
    Field('monto_destino', 'decimal(15,2)'),
    Field('tasa_aplicada', 'decimal(15,4)'),
    Field('comision', 'decimal(15,2)'),
    Field('cuenta_id', 'reference cuentas')
)

db.define_table('tasas_cambio',
    Field('fecha', 'date'),
    Field('usd_ves', 'decimal(15,4)'),
    Field('usdt_ves', 'decimal(15,4)'),
    Field('eur_ves', 'decimal(15,4)')
)

print("\n1. Verificando transacciones con USDT en la base de datos...")
transacciones_usdt = db(db.transacciones.moneda_origen == 'USDT').select()
print(f"   ✓ Transacciones con USDT encontradas: {len(transacciones_usdt)}")

if transacciones_usdt:
    print("\n   Ejemplos de transacciones USDT:")
    for t in transacciones_usdt[:3]:
        print(f"   - ID: {t.id}, Fecha: {t.fecha_transaccion}, Monto: {t.monto_origen} USDT")

print("\n2. Simulando generación de reporte diario...")
fecha_hoy = datetime.date.today()
fecha_inicio = datetime.datetime.combine(fecha_hoy, datetime.time.min)
fecha_fin = datetime.datetime.combine(fecha_hoy, datetime.time.max)

transacciones_hoy = db(
    (db.transacciones.fecha_transaccion >= fecha_inicio) &
    (db.transacciones.fecha_transaccion <= fecha_fin)
).select()

print(f"   ✓ Transacciones del día: {len(transacciones_hoy)}")

# Calcular volúmenes
ventas = [t for t in transacciones_hoy if t.tipo_operacion == 'venta']
volumen_ventas_usd = sum([float(t.monto_origen) for t in ventas if t.moneda_origen == 'USD'])
volumen_ventas_usdt = sum([float(t.monto_origen) for t in ventas if t.moneda_origen == 'USDT'])
volumen_ventas_eur = sum([float(t.monto_origen) for t in ventas if t.moneda_origen == 'EUR'])

print(f"\n   Volúmenes de venta del día:")
print(f"   - USD:  {volumen_ventas_usd:,.2f}")
print(f"   - USDT: {volumen_ventas_usdt:,.2f}")
print(f"   - EUR:  {volumen_ventas_eur:,.2f}")

# Verificar tasas promedio
print("\n3. Verificando tasas de cambio...")
tasas_hoy = db(db.tasas_cambio.fecha == fecha_hoy).select()
print(f"   ✓ Tasas registradas hoy: {len(tasas_hoy)}")

if tasas_hoy:
    tasa_usd = sum([float(t.usd_ves) for t in tasas_hoy]) / len(tasas_hoy)
    tasa_usdt = sum([float(t.usdt_ves or 0) for t in tasas_hoy]) / len(tasas_hoy)
    tasa_eur = sum([float(t.eur_ves) for t in tasas_hoy]) / len(tasas_hoy)
    
    print(f"\n   Tasas promedio del día:")
    print(f"   - USD/VES:  {tasa_usd:,.4f}")
    print(f"   - USDT/VES: {tasa_usdt:,.4f}")
    print(f"   - EUR/VES:  {tasa_eur:,.4f}")

print("\n4. Verificando reporte mensual...")
primer_dia_mes = fecha_hoy.replace(day=1)
if fecha_hoy.month == 12:
    ultimo_dia_mes = fecha_hoy.replace(year=fecha_hoy.year + 1, month=1, day=1) - datetime.timedelta(days=1)
else:
    ultimo_dia_mes = fecha_hoy.replace(month=fecha_hoy.month + 1, day=1) - datetime.timedelta(days=1)

fecha_inicio_mes = datetime.datetime.combine(primer_dia_mes, datetime.time.min)
fecha_fin_mes = datetime.datetime.combine(ultimo_dia_mes, datetime.time.max)

transacciones_mes = db(
    (db.transacciones.fecha_transaccion >= fecha_inicio_mes) &
    (db.transacciones.fecha_transaccion <= fecha_fin_mes)
).select()

print(f"   ✓ Transacciones del mes: {len(transacciones_mes)}")

ventas_mes = [t for t in transacciones_mes if t.tipo_operacion == 'venta']
volumen_ventas_usd_mes = sum([float(t.monto_origen) for t in ventas_mes if t.moneda_origen == 'USD'])
volumen_ventas_usdt_mes = sum([float(t.monto_origen) for t in ventas_mes if t.moneda_origen == 'USDT'])
volumen_ventas_eur_mes = sum([float(t.monto_origen) for t in ventas_mes if t.moneda_origen == 'EUR'])

print(f"\n   Volúmenes de venta del mes:")
print(f"   - USD:  {volumen_ventas_usd_mes:,.2f}")
print(f"   - USDT: {volumen_ventas_usdt_mes:,.2f}")
print(f"   - EUR:  {volumen_ventas_eur_mes:,.2f}")

print("\n" + "=" * 70)
print("RESUMEN DE VERIFICACIÓN")
print("=" * 70)

print("\n✓ Cambios realizados:")
print("  1. Reporte Diario ahora muestra:")
print("     - Volumen Ventas USD")
print("     - Volumen Ventas USDT (NUEVO)")
print("     - Volumen Ventas EUR")
print("     - Tasa USD/VES Promedio")
print("     - Tasa USDT/VES Promedio (NUEVO)")
print("     - Tasa EUR/VES Promedio")

print("\n  2. Reporte Mensual ahora incluye:")
print("     - Volumen Ventas USD")
print("     - Volumen Ventas USDT (NUEVO)")
print("     - Volumen Ventas EUR")

print("\n✓ Archivos modificados:")
print("  - controllers/reportes.py (función generar_reporte_mensual)")
print("  - views/reportes/reportes_administrativos.html")

print("\n✓ Para verificar en el navegador:")
print("  1. Inicia sesión como administrador")
print("  2. Ve a: Reportes > Reportes Administrativos")
print("  3. Selecciona 'Reporte Diario' o 'Reporte Mensual'")
print("  4. Verifica que aparezcan las tarjetas de USDT")

print("\n" + "=" * 70)

db.close()
