#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("=" * 80)
print("CORRECCION MANUAL DE TASA USDT")
print("=" * 80)

# Obtener la tasa activa actual
tasa_actual = db(db.tasas_cambio.activa == True).select().first()

if tasa_actual:
    print("\nTASA ACTUAL:")
    print("USD/VES: %s" % tasa_actual.usd_ves)
    print("USDT/VES: %s" % tasa_actual.usdt_ves)
    
    usd_ves = float(tasa_actual.usd_ves)
    usdt_ves_actual = float(tasa_actual.usdt_ves) if tasa_actual.usdt_ves else 0
    
    # Calcular USDT correcto (USDT aprox USD)
    usdt_ves_correcto = usd_ves * 1.0
    
    print("\nCORRECCION:")
    print("USDT/VES correcto deberia ser: %.4f" % usdt_ves_correcto)
    print("USDT/VES actual en BD: %.4f" % usdt_ves_actual)
    
    if abs(usdt_ves_correcto - usdt_ves_actual) > 1.0:
        print("\nAplicando correccion...")
        tasa_actual.update_record(usdt_ves=usdt_ves_correcto)
        db.commit()
        print("Tasa USDT corregida a: %.4f" % usdt_ves_correcto)
    else:
        print("\nLa tasa USDT ya es correcta")
else:
    print("\nNO HAY TASAS ACTIVAS")

print("\n" + "=" * 80)
