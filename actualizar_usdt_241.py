#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("=" * 80)
print("ACTUALIZACIÓN MANUAL DE TASA USDT A 241.76")
print("=" * 80)

import datetime

# Obtener la tasa activa actual
tasa_actual = db(db.tasas_cambio.activa == True).select().first()

if tasa_actual:
    print("\nTASA ACTUAL EN BD:")
    print("USD/VES: %s" % tasa_actual.usd_ves)
    print("USDT/VES: %s" % tasa_actual.usdt_ves)
    print("EUR/VES: %s" % tasa_actual.eur_ves)
    
    # Actualizar USDT a 241.76
    nuevo_usdt = 241.76
    
    print("\nACTUALIZANDO USDT/VES a %.4f..." % nuevo_usdt)
    
    tasa_actual.update_record(usdt_ves=nuevo_usdt)
    db.commit()
    
    print("✓ USDT/VES actualizado correctamente")
    
    # Verificar
    tasa_verificada = db(db.tasas_cambio.activa == True).select().first()
    print("\nTASA ACTUALIZADA:")
    print("USD/VES: %s" % tasa_verificada.usd_ves)
    print("USDT/VES: %s" % tasa_verificada.usdt_ves)
    print("EUR/VES: %s" % tasa_verificada.eur_ves)
else:
    print("\n⚠️  NO HAY TASAS ACTIVAS")
    print("Creando nueva tasa...")
    
    # Crear nueva tasa con USDT = 241.76
    db.tasas_cambio.insert(
        fecha=datetime.datetime.now(),
        hora=datetime.datetime.now().time(),
        usd_ves=231.05,
        eur_ves=267.64,
        usdt_ves=241.76,
        fuente='Manual',
        activa=True
    )
    db.commit()
    print("✓ Nueva tasa creada con USDT/VES = 241.76")

print("\n" + "=" * 80)
print("ACTUALIZACIÓN COMPLETADA")
print("Recarga la página del dashboard para ver los cambios")
print("=" * 80)
