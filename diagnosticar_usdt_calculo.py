#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Configurar path de web2py
sys.path.insert(0, r'C:\web2py')
os.chdir(r'C:\web2py')

from gluon import DAL, Field

# Conectar a la base de datos
db = DAL('sqlite://storage.sqlite', folder=r'C:\web2py\applications\sistema_divisas\databases')

# Definir tabla de tasas
db.define_table('tasas_cambio',
    Field('fecha', 'datetime'),
    Field('usd_ves', 'decimal(15,6)'),
    Field('eur_ves', 'decimal(15,6)'),
    Field('usdt_ves', 'decimal(15,6)'),
    Field('fuente', 'string'),
    Field('activa', 'boolean'),
    migrate=False
)

print("=" * 80)
print("DIAGNÓSTICO DE CÁLCULO DE USDT")
print("=" * 80)

# Obtener la tasa activa actual
tasa_actual = db(db.tasas_cambio.activa == True).select().first()

if tasa_actual:
    print("\n1. TASA ACTUAL EN LA BASE DE DATOS:")
    print(f"   USD/VES: {tasa_actual.usd_ves}")
    print(f"   EUR/VES: {tasa_actual.eur_ves}")
    print(f"   USDT/VES: {tasa_actual.usdt_ves}")
    print(f"   Fuente: {tasa_actual.fuente}")
    print(f"   Fecha: {tasa_actual.fecha}")
    
    print("\n2. ANÁLISIS DEL CÁLCULO:")
    usd_ves = float(tasa_actual.usd_ves)
    usdt_ves = float(tasa_actual.usdt_ves)
    
    # Calcular la relación
    if usdt_ves > 0:
        relacion = usd_ves / usdt_ves
        print(f"   USD/VES ÷ USDT/VES = {relacion:.4f}")
        
        if relacion > 5:
            print(f"   ⚠️  PROBLEMA DETECTADO: USDT está {relacion:.2f}x más bajo que USD")
            print(f"   ⚠️  Parece que se está dividiendo en lugar de multiplicar")
            
            print(f"\n3. VALOR CORRECTO DEBERÍA SER:")
            usdt_correcto = usd_ves * 1.0  # USDT ≈ USD
            print(f"   USDT/VES correcto: {usdt_correcto:.4f}")
            print(f"   (Asumiendo USDT/USD ≈ 1.0)")
        else:
            print(f"   ✓ El cálculo parece correcto")
    
    print("\n4. ÚLTIMAS 5 TASAS REGISTRADAS:")
    ultimas = db(db.tasas_cambio).select(
        orderby=~db.tasas_cambio.id,
        limitby=(0, 5)
    )
    for t in ultimas:
        print(f"   ID: {t.id}, USD: {t.usd_ves}, USDT: {t.usdt_ves}, Activa: {t.activa}, Fecha: {t.fecha}")
else:
    print("\n⚠️  NO HAY TASAS ACTIVAS EN LA BASE DE DATOS")

print("\n" + "=" * 80)
print("FIN DEL DIAGNÓSTICO")
print("=" * 80)

db.close()
