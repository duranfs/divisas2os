#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar que el dashboard muestre USDT correctamente
"""

import sys
import os

# Agregar el directorio de web2py al path
web2py_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, web2py_path)

# Importar módulos de web2py
from gluon import DAL, Field
from gluon.tools import Auth
from decimal import Decimal

# Conectar a la base de datos
db = DAL('sqlite://storage.sqlite', folder='databases')

# Definir las tablas necesarias
db.define_table('auth_user',
    Field('first_name'),
    Field('last_name'),
    Field('email'),
    Field('password'),
    Field('estado')
)

db.define_table('clientes',
    Field('user_id', 'reference auth_user'),
    Field('cedula'),
    Field('telefono'),
    Field('direccion')
)

db.define_table('cuentas',
    Field('cliente_id', 'reference clientes'),
    Field('numero_cuenta'),
    Field('tipo_cuenta'),
    Field('saldo_ves', 'decimal(15,2)'),
    Field('saldo_usd', 'decimal(15,2)'),
    Field('saldo_usdt', 'decimal(15,2)'),
    Field('saldo_eur', 'decimal(15,2)'),
    Field('estado')
)

db.define_table('tasas_cambio',
    Field('usd_ves', 'decimal(10,4)'),
    Field('eur_ves', 'decimal(10,4)'),
    Field('usdt_ves', 'decimal(10,4)'),
    Field('fecha', 'date'),
    Field('hora', 'time'),
    Field('fuente'),
    Field('activa', 'boolean')
)

print("=" * 70)
print("VERIFICACIÓN DEL DASHBOARD CON USDT")
print("=" * 70)

# Buscar un cliente de prueba
cliente = db(db.clientes.id > 0).select().first()

if not cliente:
    print("\n❌ No se encontró ningún cliente en el sistema")
    sys.exit(1)

print(f"\n✅ Cliente encontrado: ID {cliente.id}")

# Obtener usuario del cliente
usuario = db(db.auth_user.id == cliente.user_id).select().first()
if usuario:
    print(f"   Nombre: {usuario.first_name} {usuario.last_name}")
    print(f"   Email: {usuario.email}")

# Obtener cuentas del cliente
cuentas = db(db.cuentas.cliente_id == cliente.id).select()

if not cuentas:
    print("\n❌ El cliente no tiene cuentas")
    sys.exit(1)

print(f"\n✅ Cuentas encontradas: {len(cuentas)}")

# Calcular totales
total_ves = sum([float(cuenta.saldo_ves or 0) for cuenta in cuentas])
total_usd = sum([float(cuenta.saldo_usd or 0) for cuenta in cuentas])
total_usdt = sum([float(cuenta.saldo_usdt or 0) for cuenta in cuentas])
total_eur = sum([float(cuenta.saldo_eur or 0) for cuenta in cuentas])

print("\n" + "=" * 70)
print("RESUMEN DE SALDOS (como aparecerá en el dashboard)")
print("=" * 70)

for i, cuenta in enumerate(cuentas, 1):
    print(f"\n📊 Cuenta {i}: {cuenta.numero_cuenta}")
    print(f"   Tipo: {cuenta.tipo_cuenta}")
    print(f"   VES:  {float(cuenta.saldo_ves or 0):>12,.2f}")
    print(f"   USD:  {float(cuenta.saldo_usd or 0):>12,.2f}")
    print(f"   USDT: {float(cuenta.saldo_usdt or 0):>12,.2f}")
    print(f"   EUR:  {float(cuenta.saldo_eur or 0):>12,.2f}")

print("\n" + "=" * 70)
print("TOTALES")
print("=" * 70)
print(f"   VES:  {total_ves:>12,.2f}")
print(f"   USD:  {total_usd:>12,.2f}")
print(f"   USDT: {total_usdt:>12,.2f}")
print(f"   EUR:  {total_eur:>12,.2f}")

# Obtener tasas actuales
tasa = db(db.tasas_cambio.activa == 'T').select(
    orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora,
    limitby=(0, 1)
).first()

if not tasa:
    tasa = db().select(
        db.tasas_cambio.ALL,
        orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora,
        limitby=(0, 1)
    ).first()

if tasa:
    print("\n" + "=" * 70)
    print("TASAS DE CAMBIO ACTUALES")
    print("=" * 70)
    print(f"   USD/VES:  {float(tasa.usd_ves):>12,.4f}")
    print(f"   USDT/VES: {float(tasa.usdt_ves or 0):>12,.4f}")
    print(f"   EUR/VES:  {float(tasa.eur_ves):>12,.4f}")
    print(f"   Fuente: {tasa.fuente}")
    print(f"   Fecha: {tasa.fecha}")
    
    # Calcular equivalencia total en VES
    equivalencia_total = total_ves
    equivalencia_total += total_usd * float(tasa.usd_ves)
    if tasa.usdt_ves:
        equivalencia_total += total_usdt * float(tasa.usdt_ves)
    equivalencia_total += total_eur * float(tasa.eur_ves)
    
    print("\n" + "=" * 70)
    print("EQUIVALENCIA TOTAL EN VES")
    print("=" * 70)
    print(f"   Total: {equivalencia_total:>12,.2f} VES")
else:
    print("\n⚠️  No se encontraron tasas de cambio")

print("\n" + "=" * 70)
print("VERIFICACIÓN DE LA VISTA")
print("=" * 70)

# Verificar que la vista tenga USDT
vista_path = os.path.join('applications', 'sistema_divisas', 'views', 'default', 'dashboard.html')
if os.path.exists(vista_path):
    with open(vista_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
        
    if 'saldo_usdt' in contenido:
        print("✅ La vista dashboard.html contiene 'saldo_usdt'")
    else:
        print("❌ La vista dashboard.html NO contiene 'saldo_usdt'")
        
    if 'USDT' in contenido:
        print("✅ La vista dashboard.html muestra la etiqueta 'USDT'")
    else:
        print("❌ La vista dashboard.html NO muestra la etiqueta 'USDT'")
        
    if 'usdt_ves' in contenido:
        print("✅ La vista dashboard.html muestra la tasa 'usdt_ves'")
    else:
        print("❌ La vista dashboard.html NO muestra la tasa 'usdt_ves'")
else:
    print(f"❌ No se encontró el archivo: {vista_path}")

print("\n" + "=" * 70)
print("CONCLUSIÓN")
print("=" * 70)

if total_usdt > 0:
    print(f"✅ El cliente tiene saldo USDT: {total_usdt:,.2f}")
    print("✅ El dashboard debería mostrar este saldo correctamente")
else:
    print("⚠️  El cliente no tiene saldo USDT")
    print("   Para probar, agrega saldo USDT a una cuenta del cliente")

print("\n💡 Refresca el navegador para ver los cambios en el dashboard")
print("=" * 70)
