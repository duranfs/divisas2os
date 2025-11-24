#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Agregar el directorio de web2py al path
web2py_path = r'C:\web2py'
sys.path.insert(0, web2py_path)

os.chdir(web2py_path)

from gluon import DAL, Field
from gluon.tools import Auth

# Conectar a la base de datos
db = DAL('sqlite://storage.sqlite', folder=r'C:\web2py\applications\sistema_divisas\databases')

# Definir las tablas necesarias
db.define_table('auth_user',
    Field('first_name'),
    Field('last_name'),
    Field('email'),
    Field('username'),
    Field('password'),
    migrate=False
)

db.define_table('remesas',
    Field('fecha', 'datetime'),
    Field('monto_usd', 'decimal(15,2)'),
    Field('monto_usdt', 'decimal(15,2)'),
    Field('disponible_usd', 'decimal(15,2)'),
    Field('disponible_usdt', 'decimal(15,2)'),
    Field('activa', 'boolean'),
    Field('created_by', 'reference auth_user'),
    Field('created_on', 'datetime'),
    migrate=False
)

db.define_table('movimientos_remesas',
    Field('remesa_id', 'reference remesas'),
    Field('fecha', 'datetime'),
    Field('tipo', 'string'),
    Field('monto_usd', 'decimal(15,2)'),
    Field('monto_usdt', 'decimal(15,2)'),
    Field('descripcion', 'text'),
    Field('transaccion_id', 'reference transacciones'),
    Field('created_by', 'reference auth_user'),
    Field('created_on', 'datetime'),
    migrate=False
)

db.define_table('transacciones',
    Field('fecha', 'datetime'),
    Field('tipo', 'string'),
    Field('monto', 'decimal(15,2)'),
    migrate=False
)

print("=" * 80)
print("DIAGNÓSTICO DE MOVIMIENTOS DE REMESAS")
print("=" * 80)

# 1. Verificar remesas
print("\n1. REMESAS EN LA BASE DE DATOS:")
remesas = db(db.remesas).select(orderby=~db.remesas.id)
print(f"   Total de remesas: {len(remesas)}")
for r in remesas:
    print(f"   - ID: {r.id}, Fecha: {r.fecha}, USD: {r.monto_usd}, USDT: {r.monto_usdt}, Activa: {r.activa}")

# 2. Verificar movimientos
print("\n2. MOVIMIENTOS DE REMESAS EN LA BASE DE DATOS:")
movimientos = db(db.movimientos_remesas).select(orderby=~db.movimientos_remesas.id)
print(f"   Total de movimientos: {len(movimientos)}")
for m in movimientos:
    print(f"   - ID: {m.id}, Remesa: {m.remesa_id}, Fecha: {m.fecha}, Tipo: {m.tipo}")
    print(f"     Monto USD: {m.monto_usd}, Monto USDT: {m.monto_usdt}")
    print(f"     Descripción: {m.descripcion}")

# 3. Verificar la consulta que usa el controlador
print("\n3. SIMULANDO LA CONSULTA DEL CONTROLADOR:")
query = (db.movimientos_remesas.id > 0)
movimientos_query = db(query).select(
    db.movimientos_remesas.ALL,
    orderby=~db.movimientos_remesas.fecha,
    limitby=(0, 50)
)
print(f"   Movimientos encontrados con la query: {len(movimientos_query)}")
for m in movimientos_query:
    print(f"   - ID: {m.id}, Tipo: {m.tipo}, Fecha: {m.fecha}")

# 4. Verificar estructura de la tabla
print("\n4. ESTRUCTURA DE LA TABLA movimientos_remesas:")
for field in db.movimientos_remesas.fields:
    print(f"   - {field}: {db.movimientos_remesas[field].type}")

print("\n" + "=" * 80)
print("FIN DEL DIAGNÓSTICO")
print("=" * 80)

db.close()
