#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

db_path = r'C:\web2py\applications\divisas2os\databases\storage.sqlite'

print("=" * 80)
print("VERIFICACIÓN DE USDT EN BASE DE DATOS")
print("=" * 80)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ver todas las tasas activas
    cursor.execute("SELECT id, usd_ves, usdt_ves, eur_ves, activa, fecha FROM tasas_cambio ORDER BY id DESC LIMIT 10")
    tasas = cursor.fetchall()
    
    print("\nÚltimas 10 tasas en la base de datos:")
    print("-" * 80)
    for t in tasas:
        print(f"ID: {t[0]}, USD: {t[1]}, USDT: {t[2]}, EUR: {t[3]}, Activa: {t[4]}, Fecha: {t[5]}")
    
    # Ver específicamente la tasa activa
    cursor.execute("SELECT id, usd_ves, usdt_ves, eur_ves FROM tasas_cambio WHERE activa = 1")
    activa = cursor.fetchone()
    
    if activa:
        print("\n" + "=" * 80)
        print("TASA ACTIVA:")
        print("=" * 80)
        print(f"ID: {activa[0]}")
        print(f"USD/VES: {activa[1]}")
        print(f"USDT/VES: {activa[2]}")
        print(f"EUR/VES: {activa[3]}")
        
        if activa[2] is None:
            print("\n⚠️  USDT/VES es NULL en la base de datos")
            print("Actualizando a 241.76...")
            cursor.execute("UPDATE tasas_cambio SET usdt_ves = 241.76 WHERE id = ?", (activa[0],))
            conn.commit()
            print("✓ Actualizado")
        elif activa[2] == 241.76:
            print("\n✓ USDT/VES está correcto (241.76)")
        else:
            print(f"\n⚠️  USDT/VES tiene un valor inesperado: {activa[2]}")
    else:
        print("\n⚠️  NO HAY TASAS ACTIVAS")
    
    conn.close()
    
except Exception as e:
    print(f"\nERROR: {e}")

print("\n" + "=" * 80)
input("Presiona Enter para salir...")
