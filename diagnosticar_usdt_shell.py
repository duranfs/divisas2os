#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("=" * 80)
print("DIAGNÓSTICO DE CÁLCULO DE USDT")
print("=" * 80)

# Obtener la tasa activa actual
tasa_actual = db(db.tasas_cambio.activa == True).select().first()

if tasa_actual:
    print("\n1. TASA ACTUAL EN LA BASE DE DATOS:")
    print("   USD/VES: %s" % tasa_actual.usd_ves)
    print("   EUR/VES: %s" % tasa_actual.eur_ves)
    print("   USDT/VES: %s" % tasa_actual.usdt_ves)
    print("   Fuente: %s" % tasa_actual.fuente)
    print("   Fecha: %s" % tasa_actual.fecha)
    
    print("\n2. ANÁLISIS DEL CÁLCULO:")
    usd_ves = float(tasa_actual.usd_ves)
    usdt_ves = float(tasa_actual.usdt_ves)
    
    # Calcular la relación
    if usdt_ves > 0:
        relacion = usd_ves / usdt_ves
        print("   USD/VES / USDT/VES = %.4f" % relacion)
        
        if relacion > 5:
            print("   PROBLEMA DETECTADO: USDT está %.2fx más bajo que USD" % relacion)
            print("   Parece que se está dividiendo en lugar de multiplicar")
            
            print("\n3. VALOR CORRECTO DEBERÍA SER:")
            usdt_correcto = usd_ves * 1.0  # USDT ≈ USD
            print("   USDT/VES correcto: %.4f" % usdt_correcto)
            print("   (Asumiendo USDT/USD ≈ 1.0)")
        else:
            print("   El cálculo parece correcto")
    
    print("\n4. ÚLTIMAS 5 TASAS REGISTRADAS:")
    ultimas = db(db.tasas_cambio).select(
        orderby=~db.tasas_cambio.id,
        limitby=(0, 5)
    )
    for t in ultimas:
        print("   ID: %s, USD: %s, USDT: %s, Activa: %s" % (t.id, t.usd_ves, t.usdt_ves, t.activa))
else:
    print("\nNO HAY TASAS ACTIVAS EN LA BASE DE DATOS")

print("\n" + "=" * 80)
